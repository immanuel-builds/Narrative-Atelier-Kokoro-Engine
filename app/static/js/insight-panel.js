const POVInsight = {
    toggle() {
        const panel = document.getElementById('pov-panel');
        panel.classList.toggle('open');
        if (panel.classList.contains('open')) {
            this.refresh();
        }
    },

    async refresh() {
        const content = document.querySelector('.editor-content').value;
        if (!content.trim()) return;

        const container = document.getElementById('pov-insights');
        container.innerHTML = '<div class="analysis-loading">Observing perspective...</div>';

        try {
            const response = await fetch('/pov/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: content })
            });

            const data = await response.json();
            this.render(data);
        } catch (error) {
            console.error("POV Analysis error:", error);
            container.innerHTML = '<div class="analysis-loading">The mirror is clouded.</div>';
        }
    },

    render(data) {
        const container = document.getElementById('pov-insights');
        container.innerHTML = '';

        const { detection, intimacy, reliability } = data;

        // POV Detection
        const povItem = this.createItem(
            "Detected Perspective",
            detection.pov.replace('_', ' ').toUpperCase(),
            detection.explanation,
            "high"
        );
        container.appendChild(povItem);

        // Intimacy
        const intimacyItem = this.createItem(
            "Narrative Intimacy",
            intimacy.level,
            intimacy.description + ` (Internal: ${intimacy.internal_markers}, Sensory: ${intimacy.sensory_markers})`,
            intimacy.score > 4 ? "high" : "medium"
        );
        container.appendChild(intimacyItem);

        // Reliability
        const reliabilityItem = this.createItem(
            "Perspective Subjectivity",
            reliability.observation,
            reliability.details,
            reliability.uncertainty_score > 5 ? "medium" : "low"
        );
        container.appendChild(reliabilityItem);
    },

    createItem(title, value, details, severity) {
        const item = document.createElement('div');
        item.className = 'diagnostic-item';
        item.innerHTML = `
            <div class="diag-header" onclick="this.parentElement.classList.toggle('open')">
                <span class="diag-title">${title}: <strong>${value}</strong></span>
                <span class="diag-severity severity-${severity}">${severity}</span>
            </div>
            <div class="diag-details">
                <p>${details}</p>
            </div>
        `;
        return item;
    }
};

window.POVInsight = POVInsight;
