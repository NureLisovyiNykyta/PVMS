class CircuitBreaker {
    constructor() {
        this.state = 'CLOSED';
        this.failureCount = 0;
        this.failureThreshold = 3;
        this.openTimeout = 30000;
        this.requestTimeout = 10000;
        this.nextAttemptTime = 0;
    }


    async execute(requestFn) {
        if (this.state === 'OPEN') {
            if (Date.now() >= this.nextAttemptTime) {
                this.state = 'HALF_OPEN';
            } else {
                throw new Error('Запобіжник (Circuit Breaker) у стані OPEN. Сервіс тимчасово недоступний. Спробуйте пізніше.');
            }
        }

        try {
            const result = await requestFn();
            this.onSuccess();
            return result;
        } catch (error) {
            this.onFailure();
            throw error;
        }
    }

    onSuccess() {
        this.failureCount = 0;
        this.state = 'CLOSED';
    }

    onFailure() {
        this.failureCount++;
        if (this.state === 'HALF_OPEN' || this.failureCount >= this.failureThreshold) {
            this.state = 'OPEN';
            this.nextAttemptTime = Date.now() + this.openTimeout;
        }
    }
}

const submitBtn = document.getElementById('submitBtn');
const inputText = document.getElementById('inputText');
const resultText = document.getElementById('resultText');
const resultBox = document.getElementById('resultBox');

const circuitBreaker = new CircuitBreaker();

async function processString() {
    const value = inputText.value.trim();


    resultText.textContent = 'Processing...';
    resultText.className = '';
    resultBox.classList.remove('error-state');

    try {
        const encodedValue = encodeURIComponent(value);
        const url = `http://127.0.0.1:8000/String?value=${encodedValue}`;

        const result = await circuitBreaker.execute(async () => {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), circuitBreaker.requestTimeout);

            try {
                const response = await fetch(url, {
                    method: 'GET',
                    headers: { 'Accept': 'application/json' },
                    signal: controller.signal
                });

                clearTimeout(timeoutId);

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    const errorMessage = errorData.detail || `HTTP Error: ${response.status}`;
                    throw new Error(errorMessage);
                }

                return await response.json();
            } catch (err) {
                clearTimeout(timeoutId);
                if (err.name === 'AbortError') {
                    throw new Error('Запит перевищив час очікування (10 сек)');
                }
                throw err;
            }
        });

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