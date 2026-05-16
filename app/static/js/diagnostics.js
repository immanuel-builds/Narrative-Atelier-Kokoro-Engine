const Diagnostics = {
    init() {
        this.panel = document.getElementById('analysis-panel');
        this.resultsContainer = document.getElementById('analysis-results');
        this.textarea = document.querySelector('.editor-content');
        this.isAnalyzing = false;
    },

    toggle() {
        if (!this.panel) return;
        this.panel.classList.toggle('open');
        if (this.panel.classList.contains('open')) {
            this.runAnalysis();
        }
    },

    async runAnalysis() {
        if (!this.textarea || this.isAnalyzing) return;

        const text = this.textarea.value;
        if (!text.trim()) {
            this.renderEmpty();
            return;
        }

        this.isAnalyzing = true;
        this.renderLoading();

        try {
            const response = await fetch('/intelligence/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            const data = await response.json();
            this.renderResults(data);
        } catch (error) {
            console.error('Analysis error:', error);
            this.renderError();
        } finally {
            this.isAnalyzing = false;
        }
    },

    renderLoading() {
        this.resultsContainer.innerHTML = `
            <div class="analysis-loading">
                <div class="ai-loading-dot"></div>
                <span>The observatory is reading your narrative...</span>
            </div>
        `;
    },

    renderEmpty() {
        this.resultsContainer.innerHTML = `
            <div class="analysis-loading">
                <span>The pages are blank. Write something to begin the analysis.</span>
            </div>
        `;
    },

    renderError() {
        this.resultsContainer.innerHTML = `
            <div class="analysis-loading">
                <span>A shadow fell over the diagnostics. (Error)</span>
            </div>
        `;
    },

    renderResults(observations) {
        if (window.AnalysisSidebar) {
            AnalysisSidebar.render(observations);
        }
    }
};

window.Diagnostics = Diagnostics;
