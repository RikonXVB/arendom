document.addEventListener('DOMContentLoaded', function() {
    // Функция проверки авторизации
    async function checkAuth() {
        try {
            const response = await fetch('/api/auth/profile', {
                method: 'GET',
                headers: {
                    'Accept': 'application/json'
                }
            });
            return response.ok;
        } catch (error) {
            console.error('Ошибка проверки авторизации:', error);
            return false;
        }
    }

    // Бургер-меню
    const menuBtn = document.getElementById('menuBtn');
    const burgerMenu = document.getElementById('burgerMenu');
    const overlay = document.getElementById('overlay');

    if (menuBtn && burgerMenu && overlay) {
        menuBtn.addEventListener('click', function() {
            menuBtn.classList.toggle('active');
            burgerMenu.classList.toggle('active');
            overlay.classList.toggle('active');
        });

        overlay.addEventListener('click', function() {
            menuBtn.classList.remove('active');
            burgerMenu.classList.remove('active');
            overlay.classList.remove('active');
        });

        // Закрытие меню при клике на пункт меню
        const menuLinks = document.querySelectorAll('.burger-menu-list a');
        menuLinks.forEach(link => {
            link.addEventListener('click', function() {
                menuBtn.classList.remove('active');
                burgerMenu.classList.remove('active');
                overlay.classList.remove('active');
            });
        });
    }

    // Модальные окна
    const modal = document.getElementById('loginModal');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const profileBtn = document.querySelector('.profile-btn');
    const closeModal = document.getElementById('closeModal');
    const closeModalRegister = document.getElementById('closeModalRegister');
    const showRegister = document.getElementById('showRegister');
    const showLogin = document.getElementById('showLogin');

    function openModal(modalContent) {
        modal.classList.add('active');
        overlay.classList.add('active');
        if (modalContent === 'login') {
            loginForm.classList.add('active');
            registerForm.classList.remove('active');
        } else if (modalContent === 'register') {
            registerForm.classList.add('active');
            loginForm.classList.remove('active');
        }
    }

    function closeModals() {
        modal.classList.remove('active');
        overlay.classList.remove('active');
        loginForm.classList.remove('active');
        registerForm.classList.remove('active');
    }

    if (profileBtn) {
        profileBtn.addEventListener('click', async function(e) {
            e.preventDefault();
            const isAuthenticated = await checkAuth();
            
            if (isAuthenticated) {
                window.location.href = '/api/auth/profile';
            } else {
                openModal('login');
            }
        });
    }

    if (closeModal) {
        closeModal.addEventListener('click', closeModals);
    }

    if (closeModalRegister) {
        closeModalRegister.addEventListener('click', closeModals);
    }

    if (showRegister) {
        showRegister.addEventListener('click', function(e) {
            e.preventDefault();
            openModal('register');
        });
    }

    if (showLogin) {
        showLogin.addEventListener('click', function(e) {
            e.preventDefault();
            openModal('login');
        });
    }

    // Закрытие при клике на оверлей
    if (overlay) {
        overlay.addEventListener('click', closeModals);
    }

    // Обработка формы входа
    const loginFormElement = document.getElementById('loginFormElement');
    if (loginFormElement) {
        loginFormElement.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const emailInput = document.getElementById('login-email');
            const passwordInput = document.getElementById('login-password');
            
            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: emailInput.value.trim(),
                        password: passwordInput.value
                    })
                });

                const data = await response.json();
                
                if (response.ok) {
                    // Закрываем модальное окно
                    modal.classList.remove('active');
                    overlay.classList.remove('active');
                    
                    // Перенаправляем в профиль
                    window.location.href = '/api/auth/profile';
                } else {
                    alert(data.detail || 'Ошибка при входе');
                }
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при входе');
            }
        });
    }

    // Обработка формы регистрации
    const registerFormElement = document.getElementById('registerFormElement');
    if (registerFormElement) {
        registerFormElement.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const nameInput = document.getElementById('reg-name');
            const emailInput = document.getElementById('reg-email');
            const passwordInput = document.getElementById('reg-password');
            const confirmPasswordInput = document.getElementById('reg-confirm-password');
            
            if (passwordInput.value !== confirmPasswordInput.value) {
                alert('Пароли не совпадают');
                return;
            }
            
            try {
                const response = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        name: nameInput.value.trim(),
                        email: emailInput.value.trim(),
                        password: passwordInput.value
                    })
                });

                const data = await response.json();
                
                if (response.ok) {
                    alert('Регистрация успешна! Теперь вы можете войти.');
                    // Показываем форму входа
                    loginForm.classList.remove('hidden');
                    registerForm.classList.add('hidden');
                    // Очищаем форму
                    e.target.reset();
                } else {
                    alert(data.detail || 'Ошибка при регистрации');
                }
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при регистрации');
            }
        });
    }

    // Функция для проверки статуса избранного
    async function checkFavoriteStatus(listingId) {
        try {
            const response = await fetch(`/api/favorites/check/${listingId}`);
            const data = await response.json();
            return data.is_favorite;
        } catch (error) {
            console.error('Error checking favorite status:', error);
            return false;
        }
    }

    // Обработка клика по кнопке избранного
    const favoriteButtons = document.querySelectorAll('.favorite-toggle');
    favoriteButtons.forEach(async button => {
        const listingId = button.dataset.listingId;
        
        // Проверяем начальное состояние
        try {
            const isFavorite = await checkFavoriteStatus(listingId);
            if (isFavorite) {
                button.classList.add('active');
                const span = button.querySelector('span');
                if (span) {
                    span.textContent = 'В избранном';
                }
            }
        } catch (error) {
            console.error('Error checking initial favorite status:', error);
        }

        // Добавляем обработчик клика
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            try {
                const response = await fetch(`/api/favorites/toggle/${listingId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                if (response.ok) {
                    this.classList.toggle('active');
                    const span = this.querySelector('span');
                    if (span) {
                        span.textContent = this.classList.contains('active') ? 'В избранном' : 'Добавить в избранное';
                    }
                    
                    // Если мы на странице избранного и удаляем элемент из избранного
                    if (window.location.pathname === '/favorites' && !this.classList.contains('active')) {
                        const listingCard = this.closest('.catalog-item');
                        if (listingCard) {
                            listingCard.remove();
                            
                            // Проверяем, остались ли еще элементы
                            const remainingItems = document.querySelectorAll('.catalog-item');
                            if (remainingItems.length === 0) {
                                location.reload(); // Перезагружаем страницу, чтобы показать сообщение о пустом избранном
                            }
                        }
                    }
                }
            } catch (error) {
                console.error('Error toggling favorite:', error);
            }
        });
    });

    // Обработка клика по кнопке избранного в хедере
    const favoriteBtn = document.querySelector('.favorite-btn');
    if (favoriteBtn) {
        favoriteBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = '/favorites';
        });
    }
}); 