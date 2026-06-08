// Voice Recognition Module using Web Speech API
class VoiceRecognition {
    constructor() {
        // Check for browser support
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            console.warn('Web Speech API is not supported in this browser');
            this.isSupported = false;
            return;
        }
        
        this.isSupported = true;
        this.recognition = new SpeechRecognition();
        this.isListening = false;
        this.finalTranscript = '';
        this.interimTranscript = '';
        
        // Configure recognition
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.language = 'vi-VN'; // Vietnamese language
        
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        this.recognition.onstart = () => {
            this.isListening = true;
            this.onStart && this.onStart();
        };
        
        this.recognition.onresult = (event) => {
            this.interimTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                
                if (event.results[i].isFinal) {
                    this.finalTranscript += transcript + ' ';
                } else {
                    this.interimTranscript += transcript;
                }
            }
            
            this.onResult && this.onResult({
                final: this.finalTranscript.trim(),
                interim: this.interimTranscript.trim(),
                isFinal: event.results[event.results.length - 1].isFinal
            });
        };
        
        this.recognition.onerror = (event) => {
            this.onError && this.onError({
                error: event.error,
                message: this.getErrorMessage(event.error)
            });
        };
        
        this.recognition.onend = () => {
            this.isListening = false;
            this.onEnd && this.onEnd();
        };
    }
    
    start() {
        if (!this.isSupported) {
            console.error('Web Speech API is not supported');
            return false;
        }
        
        this.finalTranscript = '';
        this.interimTranscript = '';
        this.recognition.start();
        return true;
    }
    
    stop() {
        this.recognition.stop();
        return this.finalTranscript.trim();
    }
    
    abort() {
        this.recognition.abort();
        this.finalTranscript = '';
        this.interimTranscript = '';
    }
    
    setLanguage(lang) {
        this.recognition.language = lang;
    }
    
    getErrorMessage(errorCode) {
        const errorMessages = {
            'no-speech': 'Không phát hiện âm thanh. Vui lòng thử lại.',
            'audio-capture': 'Không tìm thấy microphone.',
            'network': 'Lỗi kết nối mạng.',
            'aborted': 'Nhận dạng đã bị dừng.',
            'service-not-allowed': 'Dịch vụ nhận dạng giọng nói không được phép.',
            'bad-grammar': 'Lỗi trong ngữ pháp nhận dạng.',
            'unknown': 'Lỗi không xác định.'
        };
        
        return errorMessages[errorCode] || 'Lỗi nhận dạng giọng nói.';
    }
}

// Create global instance
const voiceRecognition = new VoiceRecognition();
