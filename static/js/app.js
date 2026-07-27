(function () {
    const toggle = document.getElementById('theme-toggle');
    const html = document.documentElement;
    const icon = toggle?.querySelector('.theme-icon');
    const saved = localStorage.getItem('theme') || 'light';

    function applyTheme(theme) {
        html.setAttribute('data-bs-theme', theme);
        if (icon) {
            icon.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
    }

    applyTheme(saved);

    toggle?.addEventListener('click', () => {
        const next = html.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
        localStorage.setItem('theme', next);
        applyTheme(next);
    });
})();
