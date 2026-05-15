const ErrorHandler = {
    init() {
        window.addEventListener('error', (event) => {
            console.error('Global JS Error:', event.error);
            this.showToast("A small disturbance occurred in the interface. Your work remains protected.");
        });

        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled Promise Rejection:', event.reason);
            this.showToast("A connection to the observatory was interrupted. Retrying...");
        });
    },

    showToast(message) {
        // Use existing recovery toast if available, or create a simple one
        const toast = document.getElementById('recovery-toast');
        if (toast) {
            const msgEl = document.getElementById('recovery-message');
            msgEl.innerText = message;
            toast.classList.add('visible');
            setTimeout(() => toast.classList.remove('visible'), 5000);
        }
    }
};

window.ErrorHandler = ErrorHandler;
