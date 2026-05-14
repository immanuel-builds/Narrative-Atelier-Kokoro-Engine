const POVTransform = {
    openModal() {
        document.getElementById('pov-transform-modal').style.display = 'flex';
    },

    closeModal() {
        document.getElementById('pov-transform-modal').style.display = 'none';
    },

    async runTransform() {
        const targetPov = document.getElementById('target-pov-select').value;
        const content = document.querySelector('.editor-content').value;

        if (!content.trim()) {
            alert("The mirror cannot reflect an empty space. Please write something first.");
            return;
        }

        this.closeModal();

        // Show loading state (could be improved)
        const applyBtn = document.getElementById('apply-transformation');
        applyBtn.disabled = true;
        applyBtn.innerText = "Reflecting...";

        ComparisonView.open(content, "Shifting perspective...");

        try {
            const response = await fetch('/pov/transform', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: content, target_pov: targetPov })
            });

            const data = await response.json();
            if (data.transformed_text) {
                ComparisonView.updateTransformed(data.transformed_text);
                applyBtn.disabled = false;
                applyBtn.innerText = "Adopt This Perspective";

                applyBtn.onclick = () => {
                    document.querySelector('.editor-content').value = data.transformed_text;
                    ComparisonView.close();
                    if (window.Autosave) Autosave.trigger();
                    POVInsight.refresh();
                };
            } else {
                alert("The transformation was obscured. Please try again.");
                ComparisonView.close();
            }
        } catch (error) {
            console.error("POV Transformation error:", error);
            alert("A disturbance occurred in the transformation.");
            ComparisonView.close();
        }
    }
};

window.POVTransform = POVTransform;
