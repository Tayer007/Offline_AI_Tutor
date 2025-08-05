class OfflineAITutor {
    constructor() {
        this.socket = null;
        this.isConnected = false;
        this.currentTab = 'text-tutor';
        this.currentImage = null;
        this.connectionRetries = 0;
        this.maxRetries = Infinity;
        this.retryDelay = 2000;
        this.pingInterval = null;
        this.reconnectTimeout = null;
        
        // Response state - reset after every response
        this.currentStreamingMessage = null;
        this.streamingContent = '';
        this.isWaitingForResponse = false;
        
        // Settings tracking for forced reconnection
        this.lastUsedSettings = null;
        this.pendingMessage = null;
        
        this.initializeElements();
        this.setupEventListeners();
        this.connectToBackend();
    }
    
    completeStreamingResponse() {
        if (this.currentStreamingMessage) {
            console.log('✅ Completed streaming response');
        }
        this.currentStreamingMessage = null;
        this.streamingContent = '';
        
        // CRITICAL FIX: Reset the waiting state
        this.isWaitingForResponse = false;
        console.log('🔓 Reset waiting state - ready for next message');
    }

    initializeElements() {
        // Text Tutor Elements
        this.textElements = {
            chatContainer: document.getElementById('chatContainer'),
            messageInput: document.getElementById('messageInput'),
            sendTextButton: document.getElementById('sendTextButton'),
            typingIndicator: document.getElementById('typingIndicator'),
            subjectSelect: document.getElementById('subjectSelect'),
            languageSelect: document.getElementById('languageSelect'),
            levelSelect: document.getElementById('levelSelect'),
            tokenSelect: document.getElementById('tokenSelect'),
            styleSelect: document.getElementById('styleSelect'),  // ← ADD THIS
            customSubject: document.getElementById('customSubject'),
            customLanguage: document.getElementById('customLanguage'),
            customLevel: document.getElementById('customLevel'),
            customTokens: document.getElementById('customTokens'),
            customStyle: document.getElementById('customStyle')  // ← ADD THIS
        };

        // Image Analyzer Elements
        this.imageElements = {
            imageUploadArea: document.getElementById('imageUploadArea'),
            imageFileInput: document.getElementById('imageFileInput'),
            imageUrlInput: document.getElementById('imageUrlInput'),
            loadImageButton: document.getElementById('loadImageButton'),
            imagePreviewContainer: document.getElementById('imagePreviewContainer'),
            previewImage: document.getElementById('previewImage'),
            removeImageBtn: document.getElementById('removeImageBtn'),
            imageQuestionInput: document.getElementById('imageQuestionInput'),
            analyzeImageButton: document.getElementById('analyzeImageButton'),
            imageResultsContainer: document.getElementById('imageResultsContainer')
        };

        // Common Elements
        this.commonElements = {
            statusIndicator: document.getElementById('status'),
            tabButtons: document.querySelectorAll('.tab-button'),
            tabContents: document.querySelectorAll('.tab-content')
        };
    }

    setupEventListeners() {
        // Tab Navigation
        this.commonElements.tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                this.switchTab(button.dataset.tab);
            });
        });

        // Text Tutor Events
        this.setupTextTutorEvents();
        
        // Image Analyzer Events
        this.setupImageAnalyzerEvents();
    }

    setupTextTutorEvents() {
        this.textElements.sendTextButton.addEventListener('click', () => this.sendTextMessage());
        this.textElements.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendTextMessage();
            }
        });

        this.textElements.messageInput.addEventListener('input', () => {
            this.autoResizeTextarea(this.textElements.messageInput);
        });

        this.setupCustomInputHandlers();
    }

    setupImageAnalyzerEvents() {
        this.imageElements.imageUploadArea.addEventListener('click', () => {
            this.imageElements.imageFileInput.click();
        });

        this.imageElements.imageFileInput.addEventListener('change', (e) => {
            if (e.target.files[0]) {
                this.handleImageFile(e.target.files[0]);
            }
        });

        this.imageElements.loadImageButton.addEventListener('click', () => {
            this.loadImageFromUrl();
        });

        this.imageElements.imageUrlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.loadImageFromUrl();
            }
        });

        this.imageElements.removeImageBtn.addEventListener('click', () => {
            this.removeImage();
        });

        this.imageElements.analyzeImageButton.addEventListener('click', () => {
            this.analyzeImage();
        });

        document.querySelectorAll('.example-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.imageElements.imageUrlInput.value = btn.dataset.url;
                this.loadImageFromUrl();
            });
        });

        this.imageElements.imageQuestionInput.addEventListener('input', () => {
            this.autoResizeTextarea(this.imageElements.imageQuestionInput);
            this.updateAnalyzeButton();
        });

        this.setupDragAndDrop();
    }

    setupCustomInputHandlers() {
        const selects = [
            { select: this.textElements.subjectSelect, custom: this.textElements.customSubject },
            { select: this.textElements.languageSelect, custom: this.textElements.customLanguage },
            { select: this.textElements.levelSelect, custom: this.textElements.customLevel },
            { select: this.textElements.tokenSelect, custom: this.textElements.customTokens },
            { select: this.textElements.styleSelect, custom: this.textElements.customStyle } // ← ADD THIS
        ];
    
        selects.forEach(({ select, custom }) => {
            select.addEventListener('change', (e) => {
                console.log(`Dropdown changed: ${select.id} = ${e.target.value}`);
                
                if (e.target.value === 'custom') {
                    custom.style.display = 'block';
                    custom.focus();
                    console.log(`Showing custom input for ${select.id}`);
                } else {
                    custom.style.display = 'none';
                    custom.value = '';
                    console.log(`Hiding custom input for ${select.id}`);
                }
            });
            
            custom.addEventListener('blur', () => {
                // Special validation for tokens
                if (select.id === 'tokenSelect' && custom.value.trim() !== '') {
                    const tokenValue = parseInt(custom.value);
                    if (isNaN(tokenValue) || tokenValue < 50 || tokenValue > 2048) {
                        alert('Token count must be between 50 and 2048');
                        custom.focus();
                        return;
                    }
                }
                
                if (custom.value.trim() === '') {
                    select.value = select.options[0].value;
                    custom.style.display = 'none';
                    console.log(`Custom input empty, reverting ${select.id} to default`);
                }
            });
            
            custom.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    custom.blur();
                }
            });
        });
    }

    setupDragAndDrop() {
        const uploadArea = this.imageElements.imageUploadArea;
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.add('drag-over');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.remove('drag-over');
            });
        });

        uploadArea.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files[0] && files[0].type.startsWith('image/')) {
                this.handleImageFile(files[0]);
            }
        });
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    switchTab(tabName) {
        this.commonElements.tabButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });

        this.commonElements.tabContents.forEach(content => {
            content.classList.toggle('active', content.id === tabName);
        });

        this.currentTab = tabName;
    }

    // COMPLETE STATE RESET - This fixes all issues
    resetAllState() {
        console.log('🔄 RESETTING ALL STATE');
        
        // Clear streaming state
        this.currentStreamingMessage = null;
        this.streamingContent = '';
        this.isWaitingForResponse = false;
        
        // Hide typing indicator
        this.showTypingIndicator(false);
        
        // Clear any pending timeouts
        if (this.reconnectTimeout) {
            clearTimeout(this.reconnectTimeout);
            this.reconnectTimeout = null;
        }
        
        console.log('✅ State reset complete');
    }

    connectToBackend() {
        this.updateStatus('connecting', 'Connecting to AI Backend...');
        
        console.log('🔄 Attempting to connect to backend...');
        
        try {
            // Clear any existing connection
            if (this.socket) {
                this.socket.disconnect();
                this.socket = null;
            }
            
            // Clear any existing timers
            if (this.pingInterval) {
                clearInterval(this.pingInterval);
                this.pingInterval = null;
            }
            
            // Reset all state before connecting
            this.resetAllState();
            
            // Create new socket connection
            this.socket = io('http://localhost:5000', {
                forceNew: true,
                upgrade: true,
                transports: ['polling', 'websocket'],
                timeout: 18000000,
                pingTimeout: 9000000,
                pingInterval: 300000,
                reconnection: true,
                reconnectionAttempts: Infinity,
                reconnectionDelay: 2000,
                reconnectionDelayMax: 1000000000,
                maxHttpBufferSize: 1e8,
                autoConnect: true,
                rememberUpgrade: true
            });
            
            // Connection event handlers
            this.socket.on('connect', () => {
                this.isConnected = true;
                this.connectionRetries = 0;
                console.log('✅ Connected to AI Tutor backend');
                this.updateStatus('online', 'Connected - Waiting for AI models...');
                this.addSystemMessage('Connected to AI backend! 🎉 Models loading...', 'success');
                
                // Reset state on every connection
                this.resetAllState();
                this.startKeepAlive();
                
                // Send pending message if there is one (after settings change)
                if (this.pendingMessage) {
                    console.log('📤 Sending pending message after reconnection');
                    const { message, settings } = this.pendingMessage;
                    this.pendingMessage = null;
                    
                    // Wait for connection to stabilize
                    setTimeout(() => {
                        this.lastUsedSettings = { ...settings };
                        this.isWaitingForResponse = true;
                        
                        this.addTextMessage(message, 'user', settings);
                        this.showTypingIndicator(true);
                        
                        this.socket.emit('ask_ai_tutor', {
                            message: message,
                            settings: settings
                        });
                    }, 1000);
                }
            });

            this.socket.on('disconnect', (reason) => {
                this.isConnected = false;
                console.log('❌ Disconnected from backend:', reason);
                
                // Reset state on disconnect
                this.resetAllState();
                
                if (this.pingInterval) {
                    clearInterval(this.pingInterval);
                    this.pingInterval = null;
                }
                
                if (reason === 'io server disconnect') {
                    this.updateStatus('error', 'Disconnected by server');
                    this.addSystemMessage('Disconnected by server. Please restart backend.', 'error');
                } else {
                    this.updateStatus('connecting', 'Connection lost - Reconnecting...');
                    this.addSystemMessage('Connection lost. Reconnecting... 🔄', 'warning');
                }
            });

            this.socket.on('connect_error', (error) => {
                console.error('❌ Connection error:', error);
                this.updateStatus('error', 'Connection Error');
                this.addSystemMessage(`Connection error: ${error.message || error}`, 'error');
            });

            this.socket.on('reconnect', (attemptNumber) => {
                console.log(`✅ Reconnected after ${attemptNumber} attempts`);
                this.isConnected = true;
                this.updateStatus('online', 'Reconnected');
                this.addSystemMessage(`Reconnected successfully! 🎉`, 'success');
                
                // Reset state on reconnect
                this.resetAllState();
                this.startKeepAlive();
            });

            this.socket.on('reconnect_attempt', (attemptNumber) => {
                console.log(`🔄 Reconnection attempt #${attemptNumber}`);
                this.updateStatus('connecting', `Reconnecting... (${attemptNumber})`);
                
                if (attemptNumber % 5 === 0) {
                    this.addSystemMessage(`Still trying to reconnect... (attempt ${attemptNumber})`, 'warning');
                }
            });

            // Application-specific event handlers
            this.socket.on('connection_established', (data) => {
                this.handleConnectionEstablished(data);
            });

            this.socket.on('model_loading_status', (data) => {
                console.log('📡 Loading status:', data.message);
                this.updateStatus('connecting', 'Loading AI Models...');
                this.addSystemMessage(data.message, 'info');
            });

            this.socket.on('keep_alive', (data) => {
                console.log('💓 Keep-alive received:', data.status);
            });

            // SIMPLIFIED MESSAGE HANDLING - No complex state tracking
            this.socket.on('text_response_start', (data) => {
                console.log('\n' + '='.repeat(80));
                console.log('📨 RECEIVED: text_response_start');
                console.log('📥 Data:', data);
                console.log('🕐 Received at:', new Date().toISOString());
                console.log('🔍 Current streaming message exists:', !!this.currentStreamingMessage);
                console.log('='.repeat(80));
                
                this.showTypingIndicator(false);
                this.currentStreamingMessage = this.addTextMessage('', 'assistant');
                this.streamingContent = '';
                
                console.log('✅ Started new streaming message');
            });

            this.socket.on('text_response_chunk', (data) => {
                console.log('\n' + '='.repeat(80));
                console.log('📨 RECEIVED: text_response_chunk');
                console.log('📥 Message ID:', data.message_id);
                console.log('📏 Content length:', data.content?.length || 0);
                console.log('📄 Content preview:', data.content?.substring(0, 100) + '...');
                console.log('🕐 Received at:', new Date().toISOString());
                console.log('🔍 Current streaming message exists:', !!this.currentStreamingMessage);
                console.log('='.repeat(80));
                
                if (this.currentStreamingMessage) {
                    const contentDiv = this.currentStreamingMessage.querySelector('.message-text');
                    if (contentDiv) {
                        contentDiv.innerHTML = this.formatMessage(data.content);
                        this.scrollToBottom(this.textElements.chatContainer);
                        console.log('✅ Message content updated in DOM');
                    } else {
                        console.error('❌ Could not find message content div');
                    }
                } else {
                    console.error('❌ No current streaming message to update');
                    // Emergency: create message
                    this.currentStreamingMessage = this.addTextMessage(data.content, 'assistant');
                    console.log('🆘 Created emergency message');
                }
            });
            
            this.socket.on('text_response_complete', (data) => {
                console.log('\n' + '='.repeat(80));
                console.log('📨 RECEIVED: text_response_complete');
                console.log('📥 Data:', data);
                console.log('🕐 Received at:', new Date().toISOString());
                console.log('='.repeat(80));
                
                this.currentStreamingMessage = null;
                this.streamingContent = '';
                console.log('✅ Streaming completed and reset');
                this.completeStreamingResponse();
            });

            this.socket.on('image_analysis_result', (data) => {
                this.displayImageAnalysisResult(data.result);
            });

            this.socket.on('error', (data) => {
                this.handleError(data.message, data.context);
                // Reset state after error
                this.resetAllState();
            });

            this.socket.on('pong', (data) => {
                console.log('🏓 Pong received');
            });

        } catch (error) {
            console.error('❌ Failed to create socket connection:', error);
            this.updateStatus('error', 'Connection Failed');
            this.addSystemMessage('Failed to create connection. Please try refreshing.', 'error');
        }
    }

    startKeepAlive() {
        if (this.pingInterval) {
            clearInterval(this.pingInterval);
        }
        
        this.pingInterval = setInterval(() => {
            if (this.socket && this.socket.connected) {
                console.log('🏓 Sending ping...');
                this.socket.emit('ping', { timestamp: Date.now() });
            }
        }, 15000);
    }

    handleConnectionEstablished(data) {
        const tutorStatus = data.tutor_status;
        const imageStatus = data.image_analyzer_status;
        
        console.log('🔗 Connection established:', { tutorStatus, imageStatus });
        
        if (tutorStatus === 'ready' && imageStatus === 'ready') {
            this.updateStatus('online', 'AI Models Ready (Text + Images)');
            this.addSystemMessage('✅ All AI models loaded! Ready for questions! 🤖📷', 'success');
        } else if (tutorStatus === 'ready') {
            this.updateStatus('online', 'AI Models Ready (Text Only)');
            this.addSystemMessage('✅ Text AI model loaded! Ready for questions! 🤖', 'success');
            this.disableImageFeatures();
        } else if (tutorStatus === 'loading') {
            this.updateStatus('connecting', 'AI Models Loading...');
            this.addSystemMessage('⏳ AI models are still loading. Please wait...', 'info');
        } else {
            this.updateStatus('error', 'AI Models Failed');
            this.addSystemMessage('❌ AI models failed to load. Please restart backend.', 'error');
        }
    }

    disableImageFeatures() {
        const imageTab = document.querySelector('[data-tab="image-analyzer"]');
        if (imageTab) {
            imageTab.style.opacity = '0.5';
            imageTab.style.pointerEvents = 'none';
            imageTab.title = 'Image analysis unavailable - text-only mode';
        }
    }

    addSystemMessage(message, type = 'info') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message system-message ${type}-message`;
        
        const timestamp = new Date().toLocaleTimeString();
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-text">${message}</div>
                <div class="message-time">${timestamp}</div>
            </div>
        `;
        
        this.textElements.chatContainer.appendChild(messageDiv);
        this.scrollToBottom(this.textElements.chatContainer);
        
        if (type === 'info' && message.includes('loading')) {
            setTimeout(() => {
                if (messageDiv.parentNode) {
                    messageDiv.remove();
                }
            }, 30000);
        }
    }

    sendTextMessage() {
        const message = this.textElements.messageInput.value.trim();
        if (!message) {
            this.addSystemMessage('Please enter a message', 'warning');
            return;
        }
        
        if (!this.isConnected) {
            this.addSystemMessage('Not connected to backend. Please wait for connection.', 'error');
            return;
        }

        if (this.isWaitingForResponse) {
            this.addSystemMessage('Please wait for current response to complete', 'warning');
            return;
        }

        const settings = this.getCurrentTextSettings();
        
        // CHECK IF SETTINGS CHANGED - If so, force reconnection
        if (this.lastUsedSettings && this.settingsChanged(this.lastUsedSettings, settings)) {
            console.log('🔄 Settings changed, forcing reconnection...');
            this.addSystemMessage('Settings changed - reconnecting for stability...', 'info');
            
            // Store message and settings for after reconnection
            this.pendingMessage = { message, settings };
            
            // Force complete reconnection
            this.forceReconnection();
            return;
        }
        
        // Store current settings
        this.lastUsedSettings = { ...settings };
        
        // RESET STATE before sending new message
        this.resetAllState();
        
        // Mark as waiting
        this.isWaitingForResponse = true;
        
        console.log('📤 Sending message with settings:', settings);
        
        this.addTextMessage(message, 'user', settings);
        this.textElements.messageInput.value = '';
        this.autoResizeTextarea(this.textElements.messageInput);
        this.showTypingIndicator(true);
        
        this.socket.emit('ask_ai_tutor', {
            message: message,
            settings: settings
        });
    }

    settingsChanged(oldSettings, newSettings) {
        return (
            oldSettings.subject !== newSettings.subject ||
            oldSettings.language !== newSettings.language ||
            oldSettings.level !== newSettings.level ||
            oldSettings.response_style !== newSettings.response_style
        );
    }

    forceReconnection() {
        console.log('🔄 FORCING COMPLETE RECONNECTION');
        
        // Disconnect current socket
        if (this.socket) {
            this.socket.disconnect();
            this.socket = null;
        }
        
        // Clear all timers
        if (this.pingInterval) {
            clearInterval(this.pingInterval);
            this.pingInterval = null;
        }
        
        // Reset all state
        this.resetAllState();
        this.isConnected = false;
        
        // Wait a moment then reconnect
        setTimeout(() => {
            console.log('🔄 Reconnecting after forced disconnection...');
            this.connectToBackend();
        }, 1000);
    }

    // Replace the getCurrentTextSettings() method with this improved version:

    getCurrentTextSettings() {
        const getSelectValue = (select, customInput) => {
            if (select.value === 'custom') {
                const customValue = customInput.value.trim();
                if (customValue) {
                    return customValue;
                } else {
                    // If custom is selected but empty, fall back to first option
                    console.warn(`Custom selected but empty for ${select.id}, falling back to default`);
                    return select.options[0].value;
                }
            }
            return select.value;
        };
    
        // Get max_tokens value
        const getTokenValue = () => {
            if (this.textElements.tokenSelect.value === 'custom') {
                const customValue = parseInt(this.textElements.customTokens.value.trim());
                if (!isNaN(customValue) && customValue >= 50 && customValue <= 2048) {
                    return customValue;
                } else {
                    console.warn('Invalid custom token value, falling back to 256');
                    return 256;
                }
            }
            return parseInt(this.textElements.tokenSelect.value);
        };
    
        const settings = {
            subject: getSelectValue(this.textElements.subjectSelect, this.textElements.customSubject),
            language: getSelectValue(this.textElements.languageSelect, this.textElements.customLanguage),
            level: getSelectValue(this.textElements.levelSelect, this.textElements.customLevel),
            max_tokens: getTokenValue(),
            response_style: getSelectValue(this.textElements.styleSelect, this.textElements.customStyle)  // ← ADD THIS
        };
        
        console.log('Current settings:', settings);
        return settings;
    }

    addTextMessage(content, sender, settings = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const timestamp = new Date().toLocaleTimeString();
        
        let settingsHtml = '';
        if (settings && sender === 'user') {
            // Add response style to the settings display
            const styleDisplay = settings.response_style === 'regular' ? 'Regular' : 
                               settings.response_style === 'effective' ? 'Effective' : 
                               settings.response_style;
            
            settingsHtml = `
                <div class="message-settings">
                    📚 ${settings.subject} • 🌍 ${settings.language} • 🎓 ${settings.level} • 🎯 ${styleDisplay}
                </div>
            `;
        }
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-text">${this.formatMessage(content)}</div>
                ${settingsHtml}
                <div class="message-time">${timestamp}</div>
            </div>
        `;
        
        this.textElements.chatContainer.appendChild(messageDiv);
        this.scrollToBottom(this.textElements.chatContainer);
        
        return messageDiv;
    }

    handleImageFile(file) {
        if (!file.type.startsWith('image/')) {
            this.addSystemMessage('Please select a valid image file.', 'error');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            this.displayImagePreview(e.target.result);
            this.currentImage = e.target.result;
            this.updateAnalyzeButton();
        };
        reader.readAsDataURL(file);
    }

    loadImageFromUrl() {
        const url = this.imageElements.imageUrlInput.value.trim();
        if (!url) return;

        try {
            new URL(url);
        } catch {
            this.addSystemMessage('Please enter a valid image URL.', 'error');
            return;
        }

        this.displayImagePreview(url);
        this.currentImage = url;
        this.updateAnalyzeButton();
    }

    displayImagePreview(src) {
        this.imageElements.previewImage.src = src;
        this.imageElements.imagePreviewContainer.style.display = 'block';
        this.imageElements.imageUploadArea.style.display = 'none';
    }

    removeImage() {
        this.currentImage = null;
        this.imageElements.imagePreviewContainer.style.display = 'none';
        this.imageElements.imageUploadArea.style.display = 'block';
        this.imageElements.imageUrlInput.value = '';
        this.updateAnalyzeButton();
    }

    updateAnalyzeButton() {
        const hasImage = this.currentImage !== null;
        const hasQuestion = this.imageElements.imageQuestionInput.value.trim() !== '';
        this.imageElements.analyzeImageButton.disabled = !(hasImage && hasQuestion && this.isConnected);
    }

    analyzeImage() {
        if (!this.currentImage || !this.isConnected) return;

        const question = this.imageElements.imageQuestionInput.value.trim();
        if (!question) return;

        this.imageElements.analyzeImageButton.disabled = true;
        this.imageElements.analyzeImageButton.innerHTML = `
            <span class="analyze-icon">⏳</span>
            <span class="analyze-text">Analyzing...</span>
        `;

        console.log('📤 Sending image analysis request...');
        this.socket.emit('ask_image_question', {
            image_url: this.currentImage,
            question: question
        });
    }

    displayImageAnalysisResult(result) {
        this.imageElements.analyzeImageButton.disabled = false;
        this.imageElements.analyzeImageButton.innerHTML = `
            <span class="analyze-icon">🔍</span>
            <span class="analyze-text">Analyze Image</span>
        `;

        const resultDiv = document.createElement('div');
        resultDiv.className = 'analysis-result';
        resultDiv.innerHTML = `
            <div class="result-header">
                <h3>🔍 Analysis Result</h3>
                <div class="result-time">${new Date().toLocaleTimeString()}</div>
            </div>
            <div class="result-question">
                <strong>Question:</strong> ${this.imageElements.imageQuestionInput.value}
            </div>
            <div class="result-answer">
                <strong>Answer:</strong> ${this.formatMessage(result)}
            </div>
        `;

        this.imageElements.imageResultsContainer.appendChild(resultDiv);
        this.scrollToBottom(this.imageElements.imageResultsContainer);

        this.imageElements.imageQuestionInput.value = '';
        this.updateAnalyzeButton();
    }

    formatMessage(text) {
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
    }

    showTypingIndicator(show) {
        this.textElements.typingIndicator.style.display = show ? 'flex' : 'none';
        if (show) this.scrollToBottom(this.textElements.chatContainer);
    }

    handleError(message, context) {
        console.error(`❌ Error in ${context}:`, message);
        
        if (context === 'text-tutor') {
            this.showTypingIndicator(false);
            this.addTextMessage(`❌ Error: ${message}`, 'system');
        } else if (context === 'image-analyzer') {
            this.imageElements.analyzeImageButton.disabled = false;
            this.imageElements.analyzeImageButton.innerHTML = `
                <span class="analyze-icon">🔍</span>
                <span class="analyze-text">Analyze Image</span>
            `;
            this.addSystemMessage(`Image analysis error: ${message}`, 'error');
        } else {
            this.addSystemMessage(`Error: ${message}`, 'error');
        }
    }

    updateStatus(status, text) {
        this.commonElements.statusIndicator.className = `status-indicator ${status}`;
        this.commonElements.statusIndicator.nextElementSibling.textContent = text;
        
        console.log(`📊 Status updated: ${status} - ${text}`);
    }

    autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    scrollToBottom(container) {
        container.scrollTop = container.scrollHeight;
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Initializing AI Tutor frontend...');
    new OfflineAITutor();
});