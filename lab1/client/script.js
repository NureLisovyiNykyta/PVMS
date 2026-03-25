const submitBtn = document.getElementById('submitBtn');
const inputText = document.getElementById('inputText');
const resultText = document.getElementById('resultText');
const resultBox = document.getElementById('resultBox');

async function processString() {
    const value = inputText.value.trim();

    resultText.textContent = 'Processing...';
    resultText.className = '';
    resultBox.classList.remove('error-state');

    try {
        const encodedValue = encodeURIComponent(value);
        const response = await fetch(`http://127.0.0.1:8000/String?value=${encodedValue}`, {
            method: 'GET',
            headers: { 'Accept': 'application/json' }
        });

        if (!response.ok) {
            const errorData = await response.json();
            const errorMessage = errorData.detail || `HTTP Error: ${response.status}`;
            throw new Error(errorMessage);
        }

        const result = await response.json();
        resultText.textContent = result;

    } catch (error) {
        resultText.textContent = error.message;
        resultText.className = 'error-text';
        resultBox.classList.add('error-state');
    }
}

submitBtn.addEventListener('click', processString);
inputText.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') processString();
});