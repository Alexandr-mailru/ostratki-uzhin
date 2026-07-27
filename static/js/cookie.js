(function () {
    const KEY = 'ostatki_cookie_ok';
    const banner = document.getElementById('cookie-banner');
    const acceptBtn = document.getElementById('cookie-accept');

    if (!banner || !acceptBtn) {
        return;
    }

    if (localStorage.getItem(KEY) === '1') {
        banner.classList.add('hidden');
        return;
    }

    acceptBtn.addEventListener('click', function () {
        localStorage.setItem(KEY, '1');
        banner.classList.add('hidden');
    });
})();
