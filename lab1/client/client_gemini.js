class CircuitBreaker {
    constructor(failureThreshold = 3, resetTimeoutMs = 10000, requestTimeoutMs = 5000) {
        this.state = 'CLOSED';
        this.failureThreshold = failureThreshold;
        this.resetTimeout = resetTimeoutMs;
        this.requestTimeout = requestTimeoutMs;

        this.failureCount = 0;
        this.nextAttemptTime = Date.now();
    }

    async fetchWithTimeout(url, options) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.requestTimeout);

        try {
            const response = await fetch(url, { ...options, signal: controller.signal });
            clearTimeout(timeoutId);
            return response;
        } catch (error) {
            clearTimeout(timeoutId);
            throw error;
        }
    }

    async execute(url, options) {
        if (this.state === 'OPEN') {
            if (Date.now() > this.nextAttemptTime) {
                this.state = 'HALF_OPEN';
                console.log('Circuit Breaker: Стан змінено на HALF_OPEN. Тестуємо з\'єднання...');
            } else {
                throw new Error('Сервер тимчасово недоступний. Будь ласка, зачекайте.');
            }
        }

        try {
            const response = await this.fetchWithTimeout(url, options);

            if (!response.ok) {
                let errorMessage = `HTTP Error: ${response.status}`;
                try {
                    const errorData = await response.clone().json();
                    errorMessage = errorData.detail || errorMessage;
                } catch (e) {
                }
                throw new Error(errorMessage);
            }

            this.onSuccess();
            return response;

        } catch (error) {
            this.onFailure();
            if (error.name === 'AbortError') {
                throw new Error('Перевищено час очікування відповіді від сервера (Timeout).');
            }
            throw error;
        }
    }

    onSuccess() {
        this.failureCount = 0;
        if (this.state !== 'CLOSED') {
            this.state = 'CLOSED';
            console.log('Circuit Breaker: Зєднання відновлено. Стан змінено на CLOSED.');
        }
    }

    onFailure() {
        this.failureCount++;

        if (this.state === 'HALF_OPEN' || this.failureCount >= this.failureThreshold) {
            this.state = 'OPEN';
            this.nextAttemptTime = Date.now() + this.resetTimeout;
            console.warn(`Circuit Breaker: Стан змінено на OPEN. Блокування на ${this.resetTimeout / 1000} секунд.`);
        }
    }
}


const submitBtn = document.getElementById('submitBtn');
const inputText = document.getElementById('inputText');
const resultText = document.getElementById('resultText');
const resultBox = document.getElementById('resultBox');


const apiCircuitBreaker = new CircuitBreaker(3, 10000, 5000);

async function processString() {
    const value = inputText.value.trim();
    if (!value) return;

    resultText.textContent = 'Processing...';
    resultText.className = '';
    resultBox.classList.remove('error-state');

    try {
        const encodedValue = encodeURIComponent(value);
        const url = `http://127.0.0.1:8000/String?value=${encodedValue}`;

        const response = await apiCircuitBreaker.execute(url, {
            method: 'GET',
            headers: { 'Accept': 'application/json' }
        });

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