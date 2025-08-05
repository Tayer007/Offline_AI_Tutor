const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
    // Platform information
    platform: process.platform,
    
    // File operations (if needed for future features)
    openFile: () => ipcRenderer.invoke('dialog:openFile'),
    saveFile: (content) => ipcRenderer.invoke('dialog:saveFile', content),
    
    // App control (if needed for window management)
    minimizeApp: () => ipcRenderer.send('app:minimize'),
    maximizeApp: () => ipcRenderer.send('app:maximize'),
    closeApp: () => ipcRenderer.send('app:close'),
    
    // Version information
    versions: process.versions,
    
    // AI Tutor specific APIs (if needed for file handling)
    saveConversation: (data) => ipcRenderer.invoke('tutor:saveConversation', data),
    loadConversation: () => ipcRenderer.invoke('tutor:loadConversation'),
    exportAnalysis: (data) => ipcRenderer.invoke('tutor:exportAnalysis', data),
});

// Security: Remove any node globals
delete window.require;
delete window.exports;
delete window.module;