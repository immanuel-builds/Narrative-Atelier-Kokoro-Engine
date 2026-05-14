document.addEventListener('DOMContentLoaded', () => {
    const editorForm = document.getElementById('editor-form');
    const saveStatus = document.getElementById('save-status');
    const contentArea = document.querySelector('.editor-content');
    const titleArea = document.querySelector('.editor-title');

    if (!editorForm) return;

    let timeout = null;

    const handleInput = () => {
        saveStatus.textContent = 'Unsaved changes...';

        // Simple autosave placeholder logic
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            // In a real app, we would send an AJAX request here
            // saveStatus.textContent = 'Autosaving...';
            // Mocking autosave feedback
            saveStatus.textContent = 'Draft cached';
        }, 2000);
    };

    contentArea.addEventListener('input', handleInput);
    titleArea.addEventListener('input', handleInput);

    // Focus content area if title is present
    if (titleArea.value && !contentArea.value) {
        contentArea.focus();
    }
});
