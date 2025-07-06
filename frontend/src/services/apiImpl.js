import { languageLearningAPI } from './api.js';

document.getElementById('summarize').addEventListener('click', async () => {
    const text = getData();
    if (!text) return;
    const targetLanguage = document.getElementById('targetLanguage').value;
    const level = document.getElementById('learnerLevel').value;
    try {
        const result = await languageLearningAPI.generateTextSummary(
            text,
            targetLanguage,
            {
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
    try {
        const result = await languageLearningAPI.generateConversation(
            text, 
            targetLanguage, 
            {
                level: level,
                numExchanges: 15
            }
        );
        console.log(result);
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