const AnalysisSidebar = {
    render(data) {
        const container = document.getElementById('analysis-results');
        if (!container) return;

        const { observations, risks, reflections, pov, tone } = data;

        container.innerHTML = `
            <div class="analysis-summary mb-6 pb-4 border-b border-indigo-100">
                <div class="flex justify-between text-xs uppercase tracking-widest text-indigo-400 mb-2">
                    <span>POV: <span class="text-indigo-900">${pov}</span></span>
                    <span>TONE: <span class="text-indigo-900">${tone}</span></span>
                </div>
            </div>
        `;

        if (risks && risks.length > 0) {
            const riskSection = document.createElement('div');
            riskSection.className = 'narrative-risks mb-6';
            riskSection.innerHTML = '<h4 class="text-xs uppercase tracking-widest text-indigo-400 mb-3">Narrative Risks</h4>';
            risks.forEach(risk => {
                const item = document.createElement('div');
                item.className = 'risk-item p-3 mb-2 bg-red-50 border-l-2 border-red-200 text-sm';
                item.innerHTML = `<strong>${risk.risk}</strong>: ${risk.observation}`;
                riskSection.appendChild(item);
            });
            container.appendChild(riskSection);
        }

        if (observations && observations.length > 0) {
            const obsSection = document.createElement('div');
            obsSection.className = 'observations-section mb-6';
            obsSection.innerHTML = '<h4 class="text-xs uppercase tracking-widest text-indigo-400 mb-3">Observations</h4>';
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
                obsSection.appendChild(item);
            });
            container.appendChild(obsSection);
        }

        if (reflections && reflections.length > 0) {
            const reflectionSection = document.createElement('div');
            reflectionSection.className = 'reflections-section mb-6';
            reflectionSection.innerHTML = '<h4 class="text-xs uppercase tracking-widest text-indigo-400 mb-3">Reflective Prompts</h4>';
            reflections.forEach(prompt => {
                const item = document.createElement('div');
                item.className = 'reflection-item p-3 mb-2 italic border border-indigo-50 text-sm text-indigo-800';
                item.innerHTML = prompt;
                reflectionSection.appendChild(item);
            });
            container.appendChild(reflectionSection);
        }

        if ((!observations || observations.length === 0) && (!risks || risks.length === 0)) {
            container.innerHTML += `
                <div class="analysis-loading">
                    <span>The observatory finds no significant disturbances in this section.</span>
                </div>
            `;
        }

        // Initialize pacing visualizer if text is long enough
        if (window.PacingVisualizer) {
             PacingVisualizer.update();
        }
    }
};

window.AnalysisSidebar = AnalysisSidebar;
