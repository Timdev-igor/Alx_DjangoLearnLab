// Toggle nav menu on small screens
document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('navToggle');
    const nav = document.getElementById('navbarNav');

    toggle.addEventListener('click', () => {
        nav.classList.toggle('show');
    });
});
