// services/api.js
const API_BASE = 'http://localhost:8000/api';

export const languageLearningAPI = {
    // Generate text summary
    async generateTextSummary(text, targetLanguage, options = {}) {
        const response = await fetch(`${API_BASE}/content/text-summary`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include', // Include cookies
            body: JSON.stringify({
                text,
                target_language: targetLanguage,
                source_language: options.sourceLanguage || 'auto',
                length: options.length || 'about 200 words',
                level: options.level || 'Intermediate'
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to generate summary');
        }
        
        return response.json();
    },
    
    // Generate conversation
    async generateConversation(scenario, targetLanguage, options = {}) {

        const response = await fetch(`${API_BASE}/content/conversation`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                scenario,
                target_language: targetLanguage,
                source_language: options.sourceLanguage || 'auto',
                length: options.length || 'about 200 words',
                level: options.level || 'Intermediate'
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to generate conversation');
        }
        
        return response.json();
    },
    
    // Upload audio file
    async uploadAudio(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${API_BASE}/upload-audio`, {
            method: 'POST',
            credentials: 'include',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Failed to upload audio');
        }
        
        return response.json();
    },
    
    // Get user history
    async getUserHistory(limit = 10) {
        const response = await fetch(`${API_BASE}/content/history?limit=${limit}`, {
            credentials: 'include'
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch history');
        }
        
        return response.json();
    }
};