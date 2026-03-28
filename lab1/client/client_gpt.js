const submitBtn = document.getElementById('submitBtn');
const inputText = document.getElementById('inputText');
const resultText = document.getElementById('resultText');
const resultBox = document.getElementById('resultBox');


class CircuitBreaker {
    constructor({
        failureThreshold = 3,
        recoveryTimeout = 5000,
        requestTimeout = 3000
    } = {}) {
        this.failureThreshold = failureThreshold;
        this.recoveryTimeout = recoveryTimeout;
        this.requestTimeout = requestTimeout;

        this.failureCount = 0;
        this.state = 'CLOSED';
        this.nextAttempt = 0;
    }

    async call(requestFn) {
        if (this.state === 'OPEN') {
            if (Date.now() > this.nextAttempt) {
                this.state = 'HALF_OPEN';
            } else {
                throw new Error('Сервер тимчасово недоступний (Circuit Open)');
            }
        }

        try {
            const response = await this._fetchWithTimeout(requestFn);

            this._onSuccess();
            return response;

        } catch (error) {
            this._onFailure();
            throw error;
        }
    }

    async _fetchWithTimeout(requestFn) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => {
            controller.abort();
        }, this.requestTimeout);

        try {
            const response = await requestFn(controller.signal);
            clearTimeout(timeoutId);
            return response;
        } catch (error) {
            clearTimeout(timeoutId);

            if (error.name === 'AbortError') {
                throw new Error('Таймаут запиту перевищено');
            }

            throw error;
        }
    }

    _onSuccess() {
        this.failureCount = 0;

        if (this.state === 'HALF_OPEN') {
            this.state = 'CLOSED';
        }
    }

    _onFailure() {
        this.failureCount++;

        if (this.failureCount >= this.failureThreshold) {
            this.state = 'OPEN';
            this.nextAttempt = Date.now() + this.recoveryTimeout;
        }
    }
}

const circuitBreaker = new CircuitBreaker({
    failureThreshold: 3,
    recoveryTimeout: 5000,
    requestTimeout: 3000
});

async function processString() {
    const value = inputText.value.trim();

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
