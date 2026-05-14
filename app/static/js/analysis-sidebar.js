const AnalysisSidebar = {
    render(observations) {
        const container = document.getElementById('analysis-results');
        if (!container) return;

        if (!observations || observations.length === 0) {
            container.innerHTML = `
                <div class="analysis-loading">
                    <span>The observatory finds no significant disturbances in this section.</span>
                </div>
            `;
            return;
        }

        container.innerHTML = '';
        observations.forEach((obs, index) => {
            const item = document.createElement('div');
            item.className = 'diagnostic-item';
            item.innerHTML = `
                <div class="diag-header" onclick="this.parentElement.classList.toggle('open')">
                    <span class="diag-title">${obs.observation}</span>
                    <span class="diag-severity severity-${obs.severity}">${obs.severity}</span>
                </div>
                <div class="diag-details">
                    <p>${obs.details}</p>
                    ${obs.prompt ? `<div class="diag-prompt">${obs.prompt}</div>` : ''}
                </div>
            `;
            container.appendChild(item);
        });

        // Initialize pacing visualizer if text is long enough
        if (window.PacingVisualizer) {
             PacingVisualizer.update();
        }
    }
};

window.AnalysisSidebar = AnalysisSidebar;
