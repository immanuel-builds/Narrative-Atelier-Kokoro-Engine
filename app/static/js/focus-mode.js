const FocusMode = {
    init() {
        this.isActive = localStorage.getItem('kokoro_focus_mode') === 'true';
        if (this.isActive) this.enable(false);
    },

    toggle() {
        if (this.isActive) {
            this.disable();
        } else {
            this.enable();
        }
    },

    enable(save = true) {
        document.body.classList.add('focus-mode');
        this.isActive = true;
        if (save) localStorage.setItem('kokoro_focus_mode', 'true');
    },

    disable() {
        document.body.classList.remove('focus-mode');
        this.isActive = false;
        localStorage.setItem('kokoro_focus_mode', 'false');
    },

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(err => {
                console.error(`Error attempting to enable full-screen mode: ${err.message}`);
            });
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }
    }
};

window.FocusMode = FocusMode;

// Handle ESC to exit Focus Mode
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        if (document.body.classList.contains('focus-mode')) {
            FocusMode.disable();
        }
    }
});
