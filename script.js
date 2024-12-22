document.addEventListener('DOMContentLoaded', function() {
    // Код для модального окна
    const modal = document.getElementById('loginModal');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const profileBtn = document.querySelector('.profile-btn');
    const closeModal = document.getElementById('closeModal');
    const closeModalRegister = document.getElementById('closeModalRegister');
    const showRegister = document.getElementById('showRegister');

    // Открытие модального окна при клике на иконку профиля
    profileBtn.addEventListener('click', function() {
        modal.classList.add('active');
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
    });

    // Закрытие модального окна
    closeModal.addEventListener('click', function() {
        modal.classList.remove('active');
    });

    closeModalRegister.addEventListener('click', function() {
        modal.classList.remove('active');
    });

    // Переключение между формами входа и регистрации
    showRegister.addEventListener('click', function(e) {
        e.preventDefault();
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
    });

    // Код для бургер меню
    const menuBtn = document.getElementById('menuBtn');
    const burgerMenu = document.getElementById('burgerMenu');
    const overlay = document.getElementById('overlay');

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

    // Обработчик для раскрывающихся секций
    document.querySelectorAll('.section-header').forEach(header => {
        header.addEventListener('click', function() {
            const content = this.nextElementSibling;
            const icon = this.querySelector('.toggle-icon');
            
            // Просто переключаем класс active
            content.classList.toggle('active');
            
            // Меняем иконку
            icon.textContent = content.classList.contains('active') ? '-' : '+';
        });
    });

    // Инициализация календаря
    flatpickr(".calendar-input", {
        locale: "ru",
        mode: "range",
        dateFormat: "d.m.Y",
        minDate: "today",
        disableMobile: true,
        theme: "dark",
        position: "below",
        onChange: function(selectedDates, dateStr, instance) {
            if (selectedDates.length === 2) {
                // Здесь можно добавить логику для обработки выбранного диапазона дат
                console.log('Выбран диапазон:', dateStr);
            }
        }
    });
}); 