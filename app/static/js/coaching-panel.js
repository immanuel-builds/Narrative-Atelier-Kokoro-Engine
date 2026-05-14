const CoachingPanel = {
    init() {
        this.panel = document.getElementById('ai-panel');
        this.suggestionBox = document.getElementById('ai-suggestions');
        this.textarea = document.querySelector('.editor-content');
    },

    toggle() {
        if (!this.panel) return;
        this.panel.classList.toggle('open');
        if (this.panel.classList.contains('open')) {
            this.refreshCritique();
        }
    },

    async refreshCritique() {
        if (!this.suggestionBox || !this.textarea) return;

        this.suggestionBox.innerHTML = '<div class="ai-loading-dot"></div> Reviewing your narrative...';

        try {
            const response = await fetch('/ai/critique', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: this.textarea.value })
            });
            const data = await response.json();
            this.suggestionBox.innerHTML = data.result;
        } catch (error) {
            this.suggestionBox.innerHTML = "A shadow fell over the observatory. (Connection Error)";
        }
    }
};

window.CoachingPanel = CoachingPanel;
