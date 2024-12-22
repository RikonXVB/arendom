// Бургер меню
document.addEventListener('DOMContentLoaded', function() {
    const menuBtn = document.querySelector('.menu-btn');
    const burgerMenu = document.querySelector('.burger-menu');
    const overlay = document.querySelector('.overlay');

    if (menuBtn && burgerMenu && overlay) {
        menuBtn.addEventListener('click', function() {
            burgerMenu.classList.toggle('active');
            overlay.classList.toggle('active');
            menuBtn.classList.toggle('active');
        });

        overlay.addEventListener('click', function() {
            burgerMenu.classList.remove('active');
            overlay.classList.remove('active');
            menuBtn.classList.remove('active');
        });
    }

    // Закрытие меню при клике на ссылку
    const menuLinks = document.querySelectorAll('.burger-menu-list a');
    menuLinks.forEach(link => {
        link.addEventListener('click', function() {
            burgerMenu.classList.remove('active');
            overlay.classList.remove('active');
            menuBtn.classList.remove('active');
        });
    });
});

// Модальные окна
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

// Закрытие модального окна при клике вне его
document.addEventListener('click', function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.classList.remove('active');
        }
    });
});

// Обработка форм
document.addEventListener('submit', function(event) {
    if (event.target.matches('.login-form, .register-form')) {
        event.preventDefault();
        // Здесь будет логика обработки форм
    }
});

// Плавная прокрутка к якорям
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
}); 