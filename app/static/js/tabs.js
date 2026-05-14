const Tabs = {
    init(projectId) {
        this.projectId = projectId;
        this.storageKey = `kokoro_tabs_${projectId}`;
        this.tabs = this.loadTabs();
        this.render();
    },

    loadTabs() {
        const stored = localStorage.getItem(this.storageKey);
        return stored ? JSON.parse(stored) : [];
    },

    saveTabs() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.tabs));
    },

    addTab(chapterId, title) {
        if (!this.tabs.find(t => t.id === chapterId)) {
            this.tabs.push({ id: chapterId, title: title });
            this.saveTabs();
            this.render();
        }
    },

    removeTab(chapterId, event) {
        if (event) event.stopPropagation();
        this.tabs = this.tabs.filter(t => t.id !== chapterId);
        this.saveTabs();
        this.render();

        // If we closed the active chapter, redirect to another open tab or workspace root
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('chapter_id') == chapterId) {
            if (this.tabs.length > 0) {
                window.location.href = `/editor/${this.projectId}?chapter_id=${this.tabs[0].id}`;
            } else {
                window.location.href = `/editor/${this.projectId}`;
            }
        }
    },

    render() {
        const container = document.getElementById('tab-bar');
        if (!container) return;

        const currentChapterId = new URLSearchParams(window.location.search).get('chapter_id');

        container.innerHTML = '';
        this.tabs.forEach(tab => {
            const tabEl = document.createElement('div');
            tabEl.className = `tab ${currentChapterId == tab.id ? 'active' : ''}`;
            tabEl.innerHTML = `
                <span>${tab.title}</span>
                <span class="tab-close" onclick="Tabs.removeTab(${tab.id}, event)">&times;</span>
            `;
            tabEl.onclick = () => {
                window.location.href = `/editor/${this.projectId}?chapter_id=${tab.id}`;
            };
            container.appendChild(tabEl);
        });
    }
};

window.Tabs = Tabs;
