import { languageLearningAPI } from './api.js';

document.getElementById('submitBtn').addEventListener('click', async () => {
    const text = getData();
    if (!text) return;
    try {
        const result = await languageLearningAPI.generateTextSummary(text, 'Spanish');
        document.getElementById('outputText').value = result.summary || JSON.stringify(result);
    } catch (e) {
        alert('Error: ' + e.message);
    }
});

document.getElementById('conversation').addEventListener('click', async (e) => {
    const text = getData();
    if (!text) return;
    try {
        const result = await languageLearningAPI.generateConversation(text, 'Spanish');
        document.getElementById('outputText').value = result.summary || JSON.stringify(result);
    } catch (e) {
        alert('Error: ' + e.message);
    }
});

function getData() {
    const inputText = document.getElementById('inputText').value;
    return inputText;
}