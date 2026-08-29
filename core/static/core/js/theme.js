(function () {
    const body = document.body;
    const toggleBtn = document.getElementById('theme-toggle');
    const label = document.getElementById('theme-toggle-label');

    // Apply saved preference on load
    const saved = localStorage.getItem('theme');
    if (saved === 'light') {
        body.classList.add('light-mode');
        label.textContent = 'Light Mode';
    }

    toggleBtn.addEventListener('click', function () {
        body.classList.toggle('light-mode');
        const isLight = body.classList.contains('light-mode');
        label.textContent = isLight ? 'Light Mode' : 'Dark Mode';
        localStorage.setItem('theme', isLight ? 'light' : 'dark');
    });
})();