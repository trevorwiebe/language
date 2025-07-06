import { languageLearningAPI } from './api.js';
document.getElementById('submitBtn').addEventListener('click', async () => {
    const text = document.getElementById('inputText').value;
    if (!text) return;
    try {
        const result = await languageLearningAPI.generateTextSummary(text, 'Spanish');
        document.getElementById('outputText').value = result.summary || JSON.stringify(result);
    } catch (e) {
        alert('Error: ' + e.message);
    }
});