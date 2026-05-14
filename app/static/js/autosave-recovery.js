const RecoveryManager = {
    init() {
        this.toast = document.getElementById('recovery-toast');
        this.message = document.getElementById('recovery-message');
        this.checkPendingRecovery();
    },

    checkPendingRecovery() {
        const editorData = document.getElementById('editor-data');
        if (!editorData) return;

        const chapterId = editorData.dataset.chapterId;
        const lastSaved = localStorage.getItem(`kokoro_recovery_ch_${chapterId}`);

        if (lastSaved) {
            this.show("An unsaved session was recovered.");
        }
    },

    show(msg) {
        this.message.innerText = msg;
        this.toast.classList.add('visible');
    },

    dismiss() {
        const chapterId = document.getElementById('editor-data').dataset.chapterId;
        localStorage.removeItem(`kokoro_recovery_ch_${chapterId}`);
        this.toast.classList.remove('visible');
    },

    restore() {
        const chapterId = document.getElementById('editor-data').dataset.chapterId;
        const recoveredContent = localStorage.getItem(`kokoro_recovery_ch_${chapterId}`);
        if (recoveredContent) {
            document.querySelector('.editor-content').value = recoveredContent;
            if (window.Autosave) Autosave.trigger();
        }
        this.dismiss();
    },

    recordSession(content) {
        const chapterId = document.getElementById('editor-data').dataset.chapterId;
        if (chapterId) {
            localStorage.setItem(`kokoro_recovery_ch_${chapterId}`, content);
        }
    }
};

window.RecoveryManager = RecoveryManager;
