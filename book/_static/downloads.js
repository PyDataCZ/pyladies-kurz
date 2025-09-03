/**
 * Chapter Download Functionality for PyLadies Course
 *
 * This script adds download buttons to chapter pages and handles
 * the download of chapter bundles (notebook + data files).
 */

class ChapterDownloadManager {
    constructor() {
        this.downloadsIndex = null;
        this.currentChapter = null;

        // Initialize when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.init());
        } else {
            this.init();
        }
    }

    async init() {
        await this.loadDownloadsIndex();
        this.detectCurrentChapter();
        this.addDownloadButton();
    }

    /**
     * Load the downloads index JSON to get available chapters
     */
    async loadDownloadsIndex() {
        try {
            const response = await fetch('/files/index.json');
            if (response.ok) {
                this.downloadsIndex = await response.json();
            }
        } catch (error) {
            console.warn('Could not load downloads index:', error);
        }
    }

    /**
     * Detect which chapter we're currently viewing based on the URL
     */
    detectCurrentChapter() {
        const path = window.location.pathname;

        // Extract chapter name from URL patterns like:
        // /pydata.pandas_core.index.html or /pydata/pandas_core/index.html
        const match = path.match(/\/pydata[.\-\/]([^.\-\/]+)[.\-\/]index\.html?$/) ||
                     path.match(/\/pydata\/([^\/]+)\/index\.html?$/);

        if (match && this.downloadsIndex) {
            const chapterName = match[1];
            if (this.downloadsIndex.chapters[chapterName]) {
                this.currentChapter = {
                    name: chapterName,
                    ...this.downloadsIndex.chapters[chapterName]
                };
            }
        }
    }

    /**
     * Add download button to the page
     */
    addDownloadButton() {
        if (!this.currentChapter) {
            return;
        }

        // Try to find existing toolbar or header to add the button
        let targetContainer = this.findButtonContainer();

        if (targetContainer) {
            const downloadBtn = this.createDownloadButton();
            targetContainer.appendChild(downloadBtn);
        }
    }

    /**
     * Find a suitable container for the download button
     */
    findButtonContainer() {
        // Try different selectors for MyST Book theme
        const selectors = [
            '.article-header-buttons',
            '.bd-header-article',
            '.bd-page-width .bd-header',
            'article header',
            '.content'
        ];

        for (const selector of selectors) {
            const element = document.querySelector(selector);
            if (element) {
                return element;
            }
        }

        // Fallback: create our own container at the top of the article
        const article = document.querySelector('article, main, .content');
        if (article) {
            const container = document.createElement('div');
            container.className = 'chapter-download-container';
            container.style.cssText = `
                display: flex;
                justify-content: flex-end;
                margin-bottom: 1rem;
                padding: 1rem 0;
                border-bottom: 1px solid #eee;
            `;
            article.insertBefore(container, article.firstChild);
            return container;
        }

        return null;
    }

    /**
     * Create the download button element
     */
    createDownloadButton() {
        const button = document.createElement('a');
        button.href = `/${this.currentChapter.url}`;
        button.className = 'btn btn-outline-primary chapter-download-btn';
        button.innerHTML = `
            <i class="fas fa-download" aria-hidden="true"></i>
            Download Chapter
        `;
        button.title = `Download ${this.currentChapter.title} with notebook and data files`;

        // Style the button
        button.style.cssText = `
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-size: 0.9rem;
            transition: background-color 0.2s;
        `;

        // Hover effect
        button.addEventListener('mouseenter', () => {
            button.style.backgroundColor = '#0056b3';
        });

        button.addEventListener('mouseleave', () => {
            button.style.backgroundColor = '#007bff';
        });

        // Track download
        button.addEventListener('click', () => {
            this.trackDownload(this.currentChapter.name);
        });

        return button;
    }

    /**
     * Track download for analytics (optional)
     */
    trackDownload(chapterName) {
        // Add analytics tracking if needed
        if (typeof gtag !== 'undefined') {
            gtag('event', 'download', {
                event_category: 'Chapter',
                event_label: chapterName,
                value: 1
            });
        }

        console.log(`Download started: ${chapterName}`);
    }
}

// Initialize the download manager
new ChapterDownloadManager();

// Also add a download all functionality
function addDownloadAllButton() {
    const navbar = document.querySelector('.navbar-nav, .bd-navbar-elements');
    if (navbar) {
        const downloadAllBtn = document.createElement('li');
        downloadAllBtn.className = 'nav-item';
        downloadAllBtn.innerHTML = `
            <a class="nav-link" href="/downloads/" title="Download all chapters">
                <i class="fas fa-download" aria-hidden="true"></i>
                All Downloads
            </a>
        `;
        navbar.appendChild(downloadAllBtn);
    }
}

// Add download all button when page loads
document.addEventListener('DOMContentLoaded', addDownloadAllButton);
