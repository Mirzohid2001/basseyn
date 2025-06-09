/**
 * CAPTCHA functionality for Basseyn website
 * Supports both text-based and image-based CAPTCHAs
 */

class CaptchaHandler {
    constructor() {
        this.sessionKey = null;
        this.isSolved = false;
        this.formSubmitHandlers = [];
        this.questionType = 'text'; // Default to text CAPTCHA
        this.selectedImages = []; // For image CAPTCHA
    }

    /**
     * Initialize CAPTCHA on forms
     * @param {string} selector - CSS selector for forms that need CAPTCHA
     */
    init(selector = '.captcha-protected-form') {
        // Find all forms that need CAPTCHA
        const forms = document.querySelectorAll(selector);
        
        forms.forEach(form => {
            // Create CAPTCHA container
            const captchaContainer = document.createElement('div');
            captchaContainer.className = 'captcha-container';
            captchaContainer.innerHTML = `
                <div class="captcha-box">
                    <div class="captcha-question"></div>
                    <div class="captcha-images-container" style="display: none;"></div>
                    <div class="captcha-input-group">
                        <input type="text" class="captcha-input" placeholder="Введите ответ">
                        <button type="button" class="captcha-refresh">
                            <i class="fas fa-sync-alt"></i>
                        </button>
                    </div>
                    <div class="captcha-verify-btn" style="display: none;">
                        <button type="button" class="btn btn-primary captcha-verify">Проверить CAPTCHA</button>
                    </div>
                    <div class="captcha-status"></div>
                </div>
            `;
            
            // Insert CAPTCHA before the submit button
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                form.insertBefore(captchaContainer, submitBtn.parentNode);
            } else {
                form.appendChild(captchaContainer);
            }
            
            // Get CAPTCHA elements
            const questionEl = captchaContainer.querySelector('.captcha-question');
            const imagesContainer = captchaContainer.querySelector('.captcha-images-container');
            const inputEl = captchaContainer.querySelector('.captcha-input');
            const refreshBtn = captchaContainer.querySelector('.captcha-refresh');
            const statusEl = captchaContainer.querySelector('.captcha-status');
            
            // Load initial CAPTCHA
            this.loadCaptcha(questionEl, imagesContainer, inputEl, statusEl);
            
            // Add refresh button handler
            refreshBtn.addEventListener('click', () => {
                this.loadCaptcha(questionEl, imagesContainer, inputEl, statusEl);
                inputEl.value = '';
                this.isSolved = false;
                this.selectedImages = [];
            });
            
            // Add input handler to verify text CAPTCHA on input change
            inputEl.addEventListener('blur', () => {
                if (this.questionType === 'text' && inputEl.value.trim() !== '') {
                    this.verifyCaptcha(inputEl.value, statusEl);
                }
            });
            
            // Add verify button handler for image CAPTCHA
            const verifyBtn = captchaContainer.querySelector('.captcha-verify');
            const verifyBtnContainer = captchaContainer.querySelector('.captcha-verify-btn');
            
            if (verifyBtn) {
                verifyBtn.addEventListener('click', () => {
                    if (this.questionType === 'image') {
                        const answer = this.selectedImages.join(',');
                        this.verifyCaptcha(answer, statusEl);
                    }
                });
            }
            
            // Add form submit handler
            const originalSubmit = form.onsubmit;
            form.onsubmit = (e) => {
                e.preventDefault();
                
                if (this.isSolved) {
                    // If CAPTCHA is solved, proceed with original submit
                    if (originalSubmit) {
                        originalSubmit.call(form, e);
                    } else {
                        form.submit();
                    }
                } else {
                    // If not solved, verify CAPTCHA first
                    let answer;
                    
                    if (this.questionType === 'text') {
                        answer = inputEl.value;
                    } else if (this.questionType === 'image') {
                        answer = this.selectedImages.join(',');
                    }
                    
                    this.verifyCaptcha(answer, statusEl, () => {
                        if (originalSubmit) {
                            originalSubmit.call(form, e);
                        } else {
                            form.submit();
                        }
                    });
                }
            };
        });
    }
    
    /**
     * Load a new CAPTCHA
     */
    loadCaptcha(questionEl, imagesContainer, inputEl, statusEl) {
        fetch('/captcha/get-captcha/')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.sessionKey = data.session_key;
                    this.questionType = data.question_type;
                    questionEl.textContent = data.question;
                    statusEl.textContent = '';
                    statusEl.className = 'captcha-status';
                    this.isSolved = false;
                    this.selectedImages = [];
                    
                    // Get verify button container
                    const verifyBtnContainer = questionEl.closest('.captcha-container').querySelector('.captcha-verify-btn');
                    
                    // Handle image CAPTCHA
                    if (data.question_type === 'image' && data.image_data) {
                        inputEl.style.display = 'none';
                        imagesContainer.style.display = 'grid';
                        imagesContainer.innerHTML = '';
                        
                        // Show verify button for image CAPTCHA
                        if (verifyBtnContainer) {
                            verifyBtnContainer.style.display = 'block';
                        }
                        
                        data.image_data.forEach((img, index) => {
                            const imgElement = document.createElement('div');
                            imgElement.className = 'captcha-image';
                            imgElement.innerHTML = `<img src="${img.url}" alt="CAPTCHA Image ${index + 1}">`;
                            imgElement.dataset.index = index;
                            
                            imgElement.addEventListener('click', () => {
                                const isSelected = imgElement.classList.contains('selected');
                                
                                if (isSelected) {
                                    imgElement.classList.remove('selected');
                                    this.selectedImages = this.selectedImages.filter(i => i !== index.toString());
                                } else {
                                    imgElement.classList.add('selected');
                                    this.selectedImages.push(index.toString());
                                }
                            });
                            
                            imagesContainer.appendChild(imgElement);
                        });
                    } else {
                        // Handle text CAPTCHA
                        inputEl.style.display = 'block';
                        imagesContainer.style.display = 'none';
                        inputEl.value = '';
                        
                        // Hide verify button for text CAPTCHA
                        if (verifyBtnContainer) {
                            verifyBtnContainer.style.display = 'none';
                        }
                    }
                } else {
                    statusEl.textContent = 'Ошибка загрузки CAPTCHA';
                    statusEl.className = 'captcha-status error';
                }
            })
            .catch(error => {
                statusEl.textContent = 'Ошибка загрузки CAPTCHA';
                statusEl.className = 'captcha-status error';
                console.error('CAPTCHA error:', error);
            });
    }
    
    /**
     * Verify CAPTCHA answer
     */
    verifyCaptcha(answer, statusEl, callback = null) {
        if (!this.sessionKey) {
            statusEl.textContent = 'Ошибка CAPTCHA: отсутствует ключ сессии';
            statusEl.className = 'captcha-status error';
            return;
        }
        
        fetch('/captcha/verify-captcha/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken')
            },
            body: JSON.stringify({
                session_key: this.sessionKey,
                answer: answer
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                statusEl.textContent = '✓ Верно';
                statusEl.className = 'captcha-status success';
                this.isSolved = true;
                
                if (callback) {
                    callback();
                }
            } else {
                statusEl.textContent = '✗ ' + (data.message || 'Неверный ответ');
                statusEl.className = 'captcha-status error';
                this.isSolved = false;
                
                // Reload CAPTCHA on failure
                if (this.questionType === 'image') {
                    const container = statusEl.closest('.captcha-container');
                    if (container) {
                        const questionEl = container.querySelector('.captcha-question');
                        const imagesContainer = container.querySelector('.captcha-images-container');
                        const inputEl = container.querySelector('.captcha-input');
                        
                        // Reload after a short delay
                        setTimeout(() => {
                            this.loadCaptcha(questionEl, imagesContainer, inputEl, statusEl);
                        }, 1500);
                    }
                }
            }
        })
        .catch(error => {
            statusEl.textContent = 'Ошибка проверки';
            statusEl.className = 'captcha-status error';
            console.error('CAPTCHA verification error:', error);
            this.isSolved = false;
        });
    }
    
    /**
     * Get CSRF cookie for Django
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

// Initialize CAPTCHA when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.captchaHandler = new CaptchaHandler();
    window.captchaHandler.init();
});
