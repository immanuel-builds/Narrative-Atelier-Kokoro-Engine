const EnhancementMenu = {
    init() {
        this.menu = document.getElementById('enhancement-menu');
        this.overlay = document.getElementById('enhancement-overlay');
        this.textarea = document.querySelector('.editor-content');

        if (!this.textarea) return;

        this.textarea.addEventListener('mouseup', (e) => this.handleSelection(e));
        document.addEventListener('mousedown', (e) => {
            if (this.menu && !this.menu.contains(e.target) && e.target !== this.textarea) {
                this.hide();
            }
        });
    },

    handleSelection(e) {
        const selection = window.getSelection().toString().trim();
        if (selection.length > 5) {
            const rect = this.textarea.getBoundingClientRect();
            // This is a simple approximation for textarea selection positioning
            // In a more robust app, one might use a mirror div or library
            this.show(e.pageX, e.pageY);
        } else {
            this.hide();
        }
    },

    show(x, y) {
        if (!this.menu) return;
        this.menu.style.display = 'flex';
        this.menu.style.left = `${x}px`;
        this.menu.style.top = `${y - 40}px`; // Above the cursor
    },

    hide() {
        if (this.menu) this.menu.style.display = 'none';
    },

    async requestEnhancement(type, mode) {
        const selection = window.getSelection().toString().trim();
        if (!selection) return;

        this.hide();
        this.showModal("Analyzing prose...", true);

        try {
            const response = await fetch('/ai/enhance', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: selection, type, mode })
            });
            const data = await response.json();
            this.showModal(data.result, false, selection);
        } catch (error) {
            this.showModal("Error connecting to AI service.", false);
        }
    },

    showModal(content, isLoading, originalText = "") {
        if (!this.overlay) return;
        this.overlay.style.display = 'flex';
        const contentArea = document.getElementById('enhancement-result');
        const applyBtn = document.getElementById('apply-enhancement');

        contentArea.innerHTML = isLoading ? '<div class="ai-loading-dot"></div> Analyzing...' : content;

        if (applyBtn) {
            applyBtn.style.display = isLoading || content.startsWith("Integrity Violation") ? 'none' : 'block';
            applyBtn.onclick = () => this.applyResult(content, originalText);
        }
    },

    applyResult(newText, oldText) {
        const content = this.textarea.value;
        this.textarea.value = content.replace(oldText, newText);
        this.overlay.style.display = 'none';
        // Trigger autosave if available
        if (window.Autosave) window.Autosave.handleInput();
    }
};

window.EnhancementMenu = EnhancementMenu;
