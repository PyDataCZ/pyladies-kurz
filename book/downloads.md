# Stažení kapitol

Zde si můžete stáhnout jednotlivé kapitoly kurzu včetně všech potřebných souborů pro místní spuštění.

Každý balíček obsahuje:
- **Jupyter notebook** s vymazanými výstupy (připravený k použití)
- **Datové soubory** a obrázky potřebné pro cvičení
- **README** s instrukcemi k spuštění

## Jak spustit stažené kapitoly

1. **Nainstalujte potřebné balíčky**:
   ```bash
   pip install jupyter pandas matplotlib seaborn numpy
   ```

2. **Rozbalte stažený ZIP soubor**

3. **Spusťte Jupyter notebook**:
   ```bash
   jupyter notebook index.ipynb
   ```

## Dostupné kapitoly ke stažení

<div id="downloads-list">
Loading available downloads...
</div>

## Potřebujete pomoc?

- Kompletní kurz online: [https://pydatacz.github.io/pyladies-kurz/](https://pydatacz.github.io/pyladies-kurz/)
- PyLadies ČR: [http://pyladies.cz/](http://pyladies.cz/)
- PyData Praha: [http://pydata.cz/](http://pydata.cz/)

<script>
// Load and display available downloads
async function loadDownloads() {
    try {
        const response = await fetch('/_downloads/index.json');
        if (!response.ok) {
            throw new Error('Downloads not available');
        }

        const data = await response.json();
        const container = document.getElementById('downloads-list');

        if (!data.chapters || Object.keys(data.chapters).length === 0) {
            container.innerHTML = '<p>Žádné kapitoly nejsou k dispozici ke stažení.</p>';
            return;
        }

        let html = '<div class="downloads-grid">';

        for (const [chapterName, info] of Object.entries(data.chapters)) {
            html += `
                <div class="download-item">
                    <h3>${info.title}</h3>
                    <p>Kapitola: <code>${chapterName}</code></p>
                    <a href="/${info.url}" class="download-btn" onclick="trackDownload('${chapterName}')">
                        <i class="fas fa-download"></i>
                        Stáhnout ${info.filename}
                    </a>
                </div>
            `;
        }

        html += '</div>';

        // Add generation info
        if (data.generated_at) {
            const date = new Date(data.generated_at).toLocaleString('cs-CZ');
            html += `<p class="generation-info">Balíčky vygenerovány: ${date}</p>`;
        }

        container.innerHTML = html;

    } catch (error) {
        console.error('Error loading downloads:', error);
        document.getElementById('downloads-list').innerHTML =
            '<p>Nepodařilo se načíst seznam ke stažení. Zkuste to později.</p>';
    }
}

function trackDownload(chapterName) {
    // Analytics tracking
    if (typeof gtag !== 'undefined') {
        gtag('event', 'download', {
            event_category: 'Chapter',
            event_label: chapterName,
            value: 1
        });
    }
    console.log(`Download started: ${chapterName}`);
}

// Load downloads when page loads
document.addEventListener('DOMContentLoaded', loadDownloads);
</script>

<style>
.downloads-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.download-item {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1.5rem;
    background: #f9f9f9;
    text-align: center;
}

.download-item h3 {
    margin-top: 0;
    color: #333;
}

.download-item p {
    color: #666;
    margin: 0.5rem 0;
}

.download-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: #007bff;
    color: white !important;
    text-decoration: none;
    border-radius: 4px;
    font-weight: 500;
    transition: background-color 0.2s;
}

.download-btn:hover {
    background: #0056b3;
    color: white !important;
}

.generation-info {
    text-align: center;
    color: #888;
    font-size: 0.9rem;
    margin-top: 2rem;
    font-style: italic;
}
</style>
