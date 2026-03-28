const submitBtn = document.getElementById('submitBtn');
const inputText = document.getElementById('inputText');
const resultText = document.getElementById('resultText');
const resultBox = document.getElementById('resultBox');

class CircuitBreaker {
    constructor({ failureThreshold = 3, recoveryTimeout = 5000, requestTimeout = 2000 } = {}) {
        this.failureThreshold = failureThreshold;
        this.recoveryTimeout = recoveryTimeout;
        this.requestTimeout = requestTimeout;

        this.failureCount = 0;
        this.state = 'CLOSED';
        this.nextAttempt = 0;
        this.isHalfOpenTesting = false;
    }

    async call(requestFn) {
        if (this.state === 'OPEN') {
            if (Date.now() > this.nextAttempt) {
                this.state = 'HALF_OPEN';
            } else {
                const remaining = Math.ceil((this.nextAttempt - Date.now()) / 1000);
                throw new Error(`🛑 Запобіжник розімкнено (OPEN). Зачекайте ${remaining} сек...`);
            }
        }

        if (this.state === 'HALF_OPEN') {
            if (this.isHalfOpenTesting) {
                throw new Error('⏳ Виконується тестовий запит до сервера... Зачекайте.');
            }
            this.isHalfOpenTesting = true;
        }

        try {
            const response = await this._fetchWithTimeout(requestFn);
            this._onSuccess();
            return response;
        } catch (error) {
            this._onFailure();

            if (error.message === 'Failed to fetch' || error instanceof TypeError) {
                throw new Error('❌ Помилка мережі: сервер вимкнено або недоступний.');
            }
            throw error;
        }
    }

    async _fetchWithTimeout(requestFn) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.requestTimeout);

        try {
            const response = await requestFn(controller.signal);
            clearTimeout(timeoutId);
            return response;
        } catch (error) {
            clearTimeout(timeoutId);
            if (error.name === 'AbortError') throw new Error('⏱ Таймаут: сервер не відповів за 2 секунди.');
            throw error;
        }
    }

    _onSuccess() {
        this.failureCount = 0;
        this.state = 'CLOSED';
        this.isHalfOpenTesting = false;
        console.log("Circuit Breaker: CLOSED (Ланцюг замкнено, сервер працює)");
    }

    _onFailure() {
        this.failureCount++;
        this.isHalfOpenTesting = false;

        if (this.failureCount >= this.failureThreshold || this.state === 'HALF_OPEN') {
            this.state = 'OPEN';
            this.nextAttempt = Date.now() + this.recoveryTimeout;
            console.error("Circuit Breaker: OPEN (Ланцюг розірвано, ліміт помилок перевищено)");
        }
    }
}

const circuitBreaker = new CircuitBreaker();

async function processString() {
    const value = inputText.value.trim();

    if (!value) {
        resultText.textContent = "Будь ласка, введіть текст.";
        resultText.className = 'error-text';
        resultBox.classList.add('error-state');
        return;
    }

    resultText.textContent = 'Processing...';
    resultText.className = '';
    resultBox.classList.remove('error-state');

    try {
        const encodedValue = encodeURIComponent(value);

        const response = await circuitBreaker.call((signal) =>
            fetch(`http://127.0.0.1:8000/String?value=${encodedValue}`, {
                method: 'GET',
                headers: { 'Accept': 'application/json' },
                signal
            })
        );

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
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