const Autosave = {
    init(form, statusElement, projectId, chapterId, draftId) {
        this.form = form;
        this.statusElement = statusElement;
        this.projectId = projectId;
        this.chapterId = chapterId;
        this.draftId = draftId;
        this.timeout = null;
        this.saveInterval = 15000; // 15 seconds

        if (!this.form) return;

        this.form.querySelectorAll('input, textarea').forEach(el => {
            el.addEventListener('input', () => this.handleInput());
        });

        // Periodic save
        setInterval(() => this.save(), this.saveInterval);
    },

    handleInput() {
        this.statusElement.textContent = 'Unsaved changes...';
        clearTimeout(this.timeout);
        this.timeout = setTimeout(() => this.save(), 2000); // Save after 2s of no typing
    },

    async save() {
        if (this.statusElement.textContent === 'All changes saved' || this.statusElement.textContent === 'Saving...') {
            return;
        }

        this.statusElement.textContent = 'Saving...';

        const formData = new FormData(this.form);

        try {
            const response = await fetch(`/editor/${this.projectId}/chapters/${this.chapterId}/autosave`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                this.statusElement.textContent = 'All changes saved';
            } else {
                this.statusElement.textContent = 'Save failed';
            }
        } catch (error) {
            console.error('Autosave error:', error);
            this.statusElement.textContent = 'Offline - check connection';
        }
    }
};

window.Autosave = Autosave;
