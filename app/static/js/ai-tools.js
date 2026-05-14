document.addEventListener('DOMContentLoaded', () => {
    // Initialize AI Modules
    if (window.EnhancementMenu) {
        EnhancementMenu.init();
    }

    if (window.CoachingPanel) {
        CoachingPanel.init();
    }

    // Handle ESC to close AI overlays
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const overlay = document.getElementById('enhancement-overlay');
            if (overlay) overlay.style.display = 'none';

            const aiPanel = document.getElementById('ai-panel');
            if (aiPanel) aiPanel.classList.remove('open');

            const enhMenu = document.getElementById('enhancement-menu');
            if (enhMenu) enhMenu.style.display = 'none';
        }
    });
});
