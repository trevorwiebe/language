import { languageLearningAPI } from './api.js';

document.getElementById('submitBtn').addEventListener('click', async () => {
    const text = getData();
    if (!text) return;
    const targetLanguage = document.getElementById('targetLanguage').value;
    try {
        const result = await languageLearningAPI.generateTextSummary(text, targetLanguage);
        document.getElementById('outputText').innerHTML = result.summary || JSON.stringify(result);
    } catch (e) {
        alert('Error: ' + e.message);
    }
});

document.getElementById('conversation').addEventListener('click', async (e) => {
    const text = getData();
    if (!text) return;
    const targetLanguage = document.getElementById('targetLanguage').value;
    try {
        const result = await languageLearningAPI.generateConversation(
            text, 
            targetLanguage, 
            {
                level: 'intermediate',
                numExchanges: 15
            }
        );
        console.log(result.conversation);
        if (Array.isArray(result.conversation)) {
            // Alternate speaker labels A/B
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