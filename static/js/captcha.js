/**
 * Captcha boshqaruvi uchun klass
 */
class CaptchaHandler {
    constructor(options = {}) {
        // Sozlamalar
        this.options = {
            formSelector: options.formSelector || 'form',
            captchaContainerSelector: options.captchaContainerSelector || '.captcha-container',
            getCaptchaUrl: options.getCaptchaUrl || '/captcha/get-captcha/',
            verifyCaptchaUrl: options.verifyCaptchaUrl || '/captcha/verify-captcha/',
            onVerified: options.onVerified || null,
            onError: options.onError || null,
            autoInit: options.autoInit !== undefined ? options.autoInit : true
        };
        
        // Asosiy o'zgaruvchilar
        this.form = document.querySelector(this.options.formSelector);
        this.captchaContainer = document.querySelector(this.options.captchaContainerSelector);
        this.sessionKey = null;
        this.captchaType = null;
        this.verified = false;
        
        // Avtomatik ishga tushirish
        if (this.options.autoInit && this.form && this.captchaContainer) {
            this.init();
        }
    }
    
    /**
     * Captcha tizimini ishga tushirish
     */
    init() {
        // Forma yuborilganda tekshirish
        this.form.addEventListener('submit', (e) => {
            if (!this.verified) {
                e.preventDefault();
                this.verifyCaptcha();
            }
        });
        
        // Captchani yuklash
        this.loadCaptcha();
    }
    
    /**
     * Yangi captchani yuklash
     */
    loadCaptcha() {
        fetch(this.options.getCaptchaUrl)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.sessionKey = data.session_key;
                    this.captchaType = data.type;
                    this.renderCaptcha(data);
                    
                    // Sessiya kalitini hidden input-ga saqlash
                    const sessionKeyInput = document.getElementById('captcha_session_key');
                    if (sessionKeyInput) {
                        sessionKeyInput.value = this.sessionKey;
                    }
                } else {
                    this.handleError('Captcha не загружена: ' + (data.error || 'Неизвестная ошибка'));
                }
            })
            .catch(error => {
                this.handleError('Captcha не загружена: ' + error.message);
            });
    }
    
    /**
     * Captchani ko'rsatish
     */
    renderCaptcha(data) {
        this.captchaContainer.innerHTML = '';
        
        // Sarlavha
        const title = document.createElement('h4');
        title.className = 'captcha-title';
        title.textContent = 'Проверка безопасности';
        this.captchaContainer.appendChild(title);
        
        if (data.type === 'text') {
            // Matnli captcha
            this.renderTextCaptcha(data);
        } else {
            // Rasmli captcha
            this.renderImageCaptcha(data);
        }
        
        // Qayta yuklash tugmasi
        const refreshButton = document.createElement('button');
        refreshButton.type = 'button';
        refreshButton.className = 'captcha-refresh-btn';
        refreshButton.innerHTML = '<i class="fas fa-sync-alt"></i> Обновить';
        refreshButton.addEventListener('click', () => this.loadCaptcha());
        this.captchaContainer.appendChild(refreshButton);
    }
    
    /**
     * Matnli captchani ko'rsatish
     */
    renderTextCaptcha(data) {
        const questionContainer = document.createElement('div');
        questionContainer.className = 'captcha-question';
        questionContainer.textContent = data.question;
        this.captchaContainer.appendChild(questionContainer);
        
        const inputContainer = document.createElement('div');
        inputContainer.className = 'captcha-input-container';
        
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'captcha-input';
        input.placeholder = 'Введите ответ';
        input.required = true;
        input.setAttribute('data-captcha-answer', '');
        
        inputContainer.appendChild(input);
        this.captchaContainer.appendChild(inputContainer);
        
        const submitButton = document.createElement('button');
        submitButton.type = 'button';
        submitButton.className = 'captcha-submit-btn';
        submitButton.textContent = 'Подтвердить';
        submitButton.addEventListener('click', () => this.verifyCaptcha());
        this.captchaContainer.appendChild(submitButton);
    }
    
    /**
     * Rasmli captchani ko'rsatish
     */
    renderImageCaptcha(data) {
        const questionContainer = document.createElement('div');
        questionContainer.className = 'captcha-question';
        questionContainer.textContent = data.question;
        this.captchaContainer.appendChild(questionContainer);
        
        const imagesContainer = document.createElement('div');
        imagesContainer.className = 'captcha-images-container';
        
        data.images.forEach(image => {
            const imageBox = document.createElement('div');
            imageBox.className = 'captcha-image-box';
            
            const img = document.createElement('img');
            img.src = image.url;
            img.alt = 'Captcha фото';
            img.dataset.imageId = image.id;
            
            imageBox.appendChild(img);
            
            imageBox.addEventListener('click', () => {
                // Tanlangan rasmni belgilash
                document.querySelectorAll('.captcha-image-box').forEach(box => {
                    box.classList.remove('selected');
                });
                imageBox.classList.add('selected');
                
                // Javobni saqlash
                const input = document.querySelector('[data-captcha-answer]');
                if (input) {
                    input.value = image.id;
                }
            });
            
            imagesContainer.appendChild(imageBox);
        });
        
        this.captchaContainer.appendChild(imagesContainer);
        
        // Yashirin input
        const input = document.createElement('input');
        input.type = 'hidden';
        input.setAttribute('data-captcha-answer', '');
        this.captchaContainer.appendChild(input);
        
        const submitButton = document.createElement('button');
        submitButton.type = 'button';
        submitButton.className = 'captcha-submit-btn';
        submitButton.textContent = 'Подтвердить';
        submitButton.addEventListener('click', () => this.verifyCaptcha());
        this.captchaContainer.appendChild(submitButton);
    }
    
    /**
     * Captcha javobini tekshirish
     */
    verifyCaptcha() {
        const answerInput = this.captchaContainer.querySelector('[data-captcha-answer]');
        
        if (!answerInput || !answerInput.value) {
            this.handleError('Пожалуйста, введите ответ');
            return;
        }
        
        const answer = answerInput.value;
        
        // CSRF tokenni olish
        const csrftoken = this.getCookie('csrftoken');
        
        fetch(this.options.verifyCaptchaUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                session_key: this.sessionKey,
                answer: answer
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.verified = true;
                this.handleSuccess('Captcha успешно пройдена');
                
                // Formani yuborish
                if (typeof this.options.onVerified === 'function') {
                    this.options.onVerified();
                } else {
                    this.form.submit();
                }
            } else {
                this.verified = false;
                this.handleError('Неправильный ответ: ' + (data.error || 'Неизвестная ошибка'));
                this.loadCaptcha(); // Yangi captcha yuklash
            }
        })
        .catch(error => {
            this.handleError('Ошибка проверки: ' + error.message);
        });
    }
    
    /**
     * Xatoni ko'rsatish
     */
    handleError(message) {
        console.error(message);
        
        // Xato xabarini ko'rsatish
        const errorElement = document.createElement('div');
        errorElement.className = 'captcha-error';
        errorElement.textContent = message;
        
        // Avvalgi xato xabarlarini o'chirish
        const oldError = this.captchaContainer.querySelector('.captcha-error');
        if (oldError) {
            oldError.remove();
        }
        
        this.captchaContainer.appendChild(errorElement);
        
        // Callback funksiyasini chaqirish
        if (typeof this.options.onError === 'function') {
            this.options.onError(message);
        }
    }
    
    /**
     * Muvaffaqiyatni ko'rsatish
     */
    handleSuccess(message) {
        console.log(message);
        
        // Muvaffaqiyat xabarini ko'rsatish
        const successElement = document.createElement('div');
        successElement.className = 'captcha-success';
        successElement.textContent = message;
        
        // Avvalgi xabarlarni o'chirish
        const oldMessages = this.captchaContainer.querySelectorAll('.captcha-error, .captcha-success');
        oldMessages.forEach(el => el.remove());
        
        this.captchaContainer.appendChild(successElement);
    }
    
    /**
     * Cookie qiymatini olish
     */
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

// Global o'zgaruvchi sifatida eksport qilish
window.CaptchaHandler = CaptchaHandler;
