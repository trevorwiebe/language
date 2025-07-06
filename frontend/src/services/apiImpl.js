import { languageLearningAPI } from './api.js';

document.getElementById('summarize').addEventListener('click', async () => {
    const text = getData();
    if (!text) return;
    const targetLanguage = document.getElementById('targetLanguage').value;
    const level = document.getElementById('learnerLevel').value;
    const length = document.getElementById('materialLength').value;
    try {
        const result = await languageLearningAPI.generateTextSummary(
            text,
            targetLanguage,
            {
                length: length,
                level: level
            }
        );
        document.getElementById('outputText').innerHTML = result.summary || JSON.stringify(result);
    } catch (e) {
        alert('Error: ' + e.message);
    }
});

document.getElementById('conversation').addEventListener('click', async (e) => {
    const text = getData();
    if (!text) return;
    const targetLanguage = document.getElementById('targetLanguage').value;
    const level = document.getElementById('learnerLevel').value;
    const length = document.getElementById('materialLength').value;

    try {
        const result = await languageLearningAPI.generateConversation(
            text, 
            targetLanguage, 
            {
                sourceLanguage: 'auto',
                length: length,
                level: level
            }
        );
        if (Array.isArray(result.conversation)) {
            const formatted = result.conversation.map((line, idx) => `${idx % 2 === 0 ? 'Person 1' : 'Person 2'}: ${line}`);
            document.getElementById('outputText').innerHTML = formatted.join('<br><br>');
        } else {
            document.getElementById('outputText').innerHTML = JSON.stringify(result);
        }
    } catch (e) {
        alert('Error: ' + e.message);
    }

});

function getData() {
    const inputText = document.getElementById('inputText').value;
    return inputText;
}