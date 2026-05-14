document.addEventListener('DOMContentLoaded', () => {
    const editorForm = document.getElementById('editor-form');
    const saveStatus = document.getElementById('save-status');
    const contentArea = document.querySelector('.editor-content');
    const titleArea = document.querySelector('.editor-title');

    // Get project/chapter/draft IDs from the UI (passed by data-attributes or variables)
    const editorData = document.getElementById('editor-data');
    if (!editorData) return;

    const projectId = editorData.dataset.projectId;
    const chapterId = editorData.dataset.chapterId;
    const draftId = editorData.dataset.draftId;

    // Initialize Modules
    if (window.Autosave && editorForm) {
        Autosave.init(editorForm, saveStatus, projectId, chapterId, draftId);
    }

    if (window.Tabs) {
        Tabs.init(projectId);
        if (chapterId && titleArea) {
            Tabs.addTab(parseInt(chapterId), titleArea.value);
        }
    }

    if (window.FocusMode) {
        FocusMode.init();
    }

    // Statistics
    const updateStats = () => {
        const text = contentArea.value || '';
        const words = text.trim() ? text.trim().split(/\s+/).length : 0;
        const chars = text.length;
        const readingTime = Math.ceil(words / 200); // 200 wpm

        document.getElementById('word-count').textContent = `${words} words`;
        document.getElementById('char-count').textContent = `${chars} chars`;
        document.getElementById('reading-time').textContent = `${readingTime} min read`;
    };

    if (contentArea) {
        contentArea.addEventListener('input', updateStats);
        updateStats(); // Initial count
    }

    // Focus content area if title is present
    if (titleArea && titleArea.value && contentArea && !contentArea.value) {
        contentArea.focus();
    }

    // Handle ESC to close modals and panels
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const modals = ['new-chapter-modal', 'new-draft-modal', 'create-modal', 'edit-modal'];
            modals.forEach(id => {
                const el = document.getElementById(id);
                if (el) el.style.display = 'none';
            });

            const draftPanel = document.getElementById('draft-panel');
            if (draftPanel) draftPanel.classList.remove('open');
        }
    });
});
