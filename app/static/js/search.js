const EditorSearch = {
    init() {
        this.input = document.getElementById('editor-search');
        this.editor = document.querySelector('.editor-content');

        if (this.input) {
            this.input.addEventListener('input', () => this.handleSearch());
        }
    },

    handleSearch() {
        const query = this.input.value.toLowerCase();
        if (!query) {
            this.clearHighlight();
            return;
        }

        // Lightweight search: just find and highlight first occurrence or scroll to it
        // Note: highlighting in a textarea is limited, so we mostly use this for filtering chapter list
        // or we could implement a more advanced overlay. For MVP, we'll filter chapters.

        document.querySelectorAll('.chapter-item').forEach(item => {
            const title = item.querySelector('span').innerText.toLowerCase();
            if (title.includes(query)) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    },

    clearHighlight() {
        document.querySelectorAll('.chapter-item').forEach(item => {
            item.style.display = 'flex';
        });
    }
};

window.EditorSearch = EditorSearch;
