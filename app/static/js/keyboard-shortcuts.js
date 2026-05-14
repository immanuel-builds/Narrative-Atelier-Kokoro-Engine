document.addEventListener('keydown', (e) => {
    // Ctrl+S: Save
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        const saveBtn = document.querySelector('button[form="editor-form"]');
        if (saveBtn) saveBtn.click();
    }

    // Ctrl+Shift+F: Focus Mode
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'F') {
        e.preventDefault();
        if (window.FocusMode) FocusMode.toggle();
    }

    // Ctrl+F: Search Focus
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        const searchInput = document.getElementById('editor-search');
        if (searchInput) {
            e.preventDefault();
            searchInput.focus();
        }
    }

    // Ctrl+N: New Chapter
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        const newChapterBtn = document.querySelector('.sidebar-header button');
        if (newChapterBtn) newChapterBtn.click();
    }
});
