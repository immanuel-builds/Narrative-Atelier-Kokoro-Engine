const ComparisonView = {
    open(original, transformed) {
        const overlay = document.getElementById('comparison-overlay');
        const originalPane = document.getElementById('original-text-pane');
        const transformedPane = document.getElementById('transformed-text-pane');

        originalPane.innerText = original;
        transformedPane.innerText = transformed;

        overlay.style.display = 'flex';
        document.body.style.overflow = 'hidden';

        this.syncScrolling(originalPane, transformedPane);
    },

    updateTransformed(text) {
        document.getElementById('transformed-text-pane').innerText = text;
    },

    close() {
        document.getElementById('comparison-overlay').style.display = 'none';
        document.body.style.overflow = '';
    },

    syncScrolling(paneA, paneB) {
        let isSyncing = false;

        paneA.onscroll = () => {
            if (!isSyncing) {
                isSyncing = true;
                paneB.scrollTop = paneA.scrollTop;
                isSyncing = false;
            }
        };

        paneB.onscroll = () => {
            if (!isSyncing) {
                isSyncing = true;
                paneA.scrollTop = paneB.scrollTop;
                isSyncing = false;
            }
        };
    }
};

window.ComparisonView = ComparisonView;
