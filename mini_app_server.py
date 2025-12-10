from aiohttp import web
import json

# Данные о странах и ценах
COUNTRIES = {
    "US": {"name": "🇺🇸 США", "price": 0.46, "code": "+1"},
    "RU": {"name": "🇷🇺 Россия", "price": 3.90, "code": "+7"},
    "GB": {"name": "🇬🇧 Великобритания", "price": 1.63, "code": "+44"},
    # ... остальные страны из вашего списка
}

OPTIONS = {
    "none": {"name": "Без опций", "multiplier": 1.0},
    "warmed": {"name": "Прогретый", "multiplier": 1.3},
    "otliga": {"name": "С отлегой", "multiplier": 1.4},
    "both": {"name": "Обе опции", "multiplier": 1.7}
}

async def handle_mini_app(request):
    """Основная страница Mini App"""
    html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nezeex Store - Telegram Accounts</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <style>
            :root {
                --primary: #0088cc;
                --secondary: #667eea;
                --success: #4ade80;
                --danger: #f87171;
                --dark: #1a1a1a;
                --light: #f8fafc;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: linear-gradient(135deg, var(--secondary) 0%, var(--primary) 100%);
                min-height: 100vh;
                color: white;
                padding: 20px;
            }
            
            .container {
                max-width: 100%;
                margin: 0 auto;
            }
            
            .header {
                text-align: center;
                padding: 25px 20px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                margin-bottom: 25px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .logo {
                font-size: 2.8em;
                margin-bottom: 10px;
            }
            
            .subtitle {
                opacity: 0.9;
                font-size: 1.1em;
                margin-bottom: 15px;
            }
            
            .status-bar {
                display: flex;
                justify-content: space-between;
                background: rgba(0, 0, 0, 0.2);
                padding: 10px 15px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            
            .step {
                display: flex;
                align-items: center;
                gap: 8px;
                opacity: 0.6;
            }
            
            .step.active {
                opacity: 1;
                font-weight: bold;
            }
            
            .step-number {
                background: var(--primary);
                width: 25px;
                height: 25px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 0.9em;
            }
            
            .section {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 25px;
                margin-bottom: 20px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .section-title {
                font-size: 1.4em;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .countries-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                gap: 15px;
                margin-bottom: 20px;
            }
            
            .country-card {
                background: rgba(255, 255, 255, 0.15);
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                border: 2px solid transparent;
            }
            
            .country-card:hover {
                background: rgba(255, 255, 255, 0.25);
                transform: translateY(-3px);
            }
            
            .country-card.selected {
                background: rgba(74, 222, 128, 0.3);
                border-color: var(--success);
            }
            
            .country-flag {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .country-name {
                font-size: 1em;
                margin-bottom: 8px;
                font-weight: bold;
            }
            
            .country-price {
                font-size: 1.1em;
                color: var(--success);
                font-weight: bold;
            }
            
            .option-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 18px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                margin-bottom: 12px;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .option-item:hover {
                background: rgba(255, 255, 255, 0.2);
            }
            
            .option-item.selected {
                background: rgba(74, 222, 128, 0.3);
                border: 2px solid var(--success);
            }
            
            .option-info {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .option-icon {
                font-size: 1.5em;
            }
            
            .option-multiplier {
                background: rgba(255, 255, 255, 0.2);
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.9em;
            }
            
            .total-section {
                text-align: center;
                padding: 25px;
            }
            
            .total-price {
                font-size: 2.5em;
                font-weight: bold;
                margin: 20px 0;
                color: var(--success);
            }
            
            .buy-button {
                width: 100%;
                padding: 22px;
                background: linear-gradient(135deg, var(--success) 0%, #22c55e 100%);
                border: none;
                border-radius: 15px;
                color: white;
                font-size: 1.3em;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 10px 20px rgba(34, 197, 94, 0.3);
            }
            
            .buy-button:hover {
                transform: scale(1.03);
                box-shadow: 0 15px 30px rgba(34, 197, 94, 0.4);
            }
            
            .buy-button:disabled {
                background: #666;
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }
            
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--success);
                color: white;
                padding: 15px 25px;
                border-radius: 10px;
                animation: slideIn 0.3s ease;
                display: none;
                z-index: 1000;
                max-width: 300px;
            }
            
            .support-links {
                display: flex;
                gap: 15px;
                justify-content: center;
                margin-top: 20px;
                flex-wrap: wrap;
            }
            
            .support-link {
                padding: 12px 20px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                text-decoration: none;
                color: white;
                transition: all 0.3s ease;
            }
            
            .support-link:hover {
                background: rgba(255, 255, 255, 0.2);
            }
            
            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @media (max-width: 600px) {
                .countries-grid {
                    grid-template-columns: repeat(2, 1fr);
                }
                
                .logo {
                    font-size: 2.2em;
                }
                
                .total-price {
                    font-size: 2em;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Шапка -->
            <div class="header">
                <div class="logo">📱 Nezeex Store</div>
                <div class="subtitle">Физ-аккаунты Telegram • Продажа с 2023</div>
                <div class="status-bar">
                    <div class="step active">
                        <div class="step-number">1</div>
                        <span>Страна</span>
                    </div>
                    <div class="step">
                        <div class="step-number">2</div>
                        <span>Опции</span>
                    </div>
                    <div class="step">
                        <div class="step-number">3</div>
                        <span>Оплата</span>
                    </div>
                </div>
            </div>
            
            <!-- Выбор страны -->
            <div class="section">
                <div class="section-title">
                    <span>🌍 Выберите страну</span>
                </div>
                <div class="countries-grid" id="countriesGrid">
                    <!-- Страны загружаются через JS -->
                </div>
            </div>
            
            <!-- Выбор опций -->
            <div class="section" id="optionsSection" style="display: none;">
                <div class="section-title">
                    <span>⚡ Дополнительные опции</span>
                </div>
                <div id="optionsList">
                    <div class="option-item" data-option="none" onclick="selectOption('none')">
                        <div class="option-info">
                            <span class="option-icon">📱</span>
                            <div>
                                <div style="font-weight: bold;">Базовый аккаунт</div>
                                <div style="font-size: 0.9em; opacity: 0.8;">Стандартная версия</div>
                            </div>
                        </div>
                        <div class="option-multiplier">×1.0</div>
                    </div>
                    
                    <div class="option-item" data-option="warmed" onclick="selectOption('warmed')">
                        <div class="option-info">
                            <span class="option-icon">🔥</span>
                            <div>
                                <div style="font-weight: bold;">Прогретый аккаунт</div>
                                <div style="font-size: 0.9em; opacity: 0.8;">С историей активности</div>
                            </div>
                        </div>
                        <div class="option-multiplier">×1.3</div>
                    </div>
                    
                    <div class="option-item" data-option="otliga" onclick="selectOption('otliga')">
                        <div class="option-info">
                            <span class="option-icon">🛡️</span>
                            <div>
                                <div style="font-weight: bold;">С отлегой (1 год)</div>
                                <div style="font-size: 0.9em; opacity: 0.8;">Защита от ограничений</div>
                            </div>
                        </div>
                        <div class="option-multiplier">×1.4</div>
                    </div>
                    
                    <div class="option-item" data-option="both" onclick="selectOption('both')">
                        <div class="option-info">
                            <span class="option-icon">🔥🛡️</span>
                            <div>
                                <div style="font-weight: bold;">Обе опции</div>
                                <div style="font-size: 0.9em; opacity: 0.8;">Максимальная защита</div>
                            </div>
                        </div>
                        <div class="option-multiplier">×1.7</div>
                    </div>
                </div>
            </div>
            
            <!-- Итого и оплата -->
            <div class="total-section" id="totalSection" style="display: none;">
                <div style="font-size: 1.2em; margin-bottom: 10px;">Итоговая стоимость:</div>
                <div class="total-price" id="totalPrice">$0.00</div>
                <button class="buy-button" id="buyButton" onclick="processPayment()">
                    💳 Оплатить $0.00
                </button>
                
                <div class="support-links">
                    <a href="https://t.me/v3estnikov" class="support-link" target="_blank">
                        👨‍💻 Поддержка
                    </a>
                    <a href="https://t.me/otzuvuvestnikaa" class="support-link" target="_blank">
                        💬 Отзывы
                    </a>
                    <a href="#" class="support-link" onclick="showInstructions()">
                        ❓ Инструкция
                    </a>
                </div>
            </div>
        </div>
        
        <!-- Уведомление -->
        <div class="notification" id="notification"></div>
        
        <script>
            // Telegram Web App
            const tg = window.Telegram.WebApp;
            
            // Данные о странах (полный список)
            const countries = """ + json.dumps(COUNTRIES) + """;
            
            // Опции
            const options = """ + json.dumps(OPTIONS) + """;
            
            // Текущий выбор
            let selectedCountry = null;
            let selectedOption = 'none';
            
            // Инициализация
            tg.expand();
            tg.ready();
            
            // Загрузка стран
            function loadCountries() {
                const grid = document.getElementById('countriesGrid');
                grid.innerHTML = '';
                
                Object.entries(countries).forEach(([code, data]) => {
                    const card = document.createElement('div');
                    card.className = 'country-card';
                    card.dataset.code = code;
                    card.innerHTML = `
                        <div class="country-flag">${data.name.split(' ')[0]}</div>
                        <div class="country-name">${data.name.split(' ').slice(1).join(' ')}</div>
                        <div class="country-price">$${data.price.toFixed(2)}</div>
                        <div style="font-size: 0.9em; opacity: 0.8;">${data.code}</div>
                    `;
                    card.onclick = () => selectCountry(code, data);
                    grid.appendChild(card);
                });
            }
            
            // Выбор страны
            function selectCountry(code, data) {
                // Снимаем выделение со всех карточек
                document.querySelectorAll('.country-card').forEach(card => {
                    card.classList.remove('selected');
                });
                
                // Выделяем выбранную
                const selectedCard = document.querySelector(`.country-card[data-code="${code}"]`);
                selectedCard.classList.add('selected');
                
                selectedCountry = {code, ...data};
                
                // Показываем опции
                document.getElementById('optionsSection').style.display = 'block';
                document.getElementById('totalSection').style.display = 'block';
                
                // Обновляем шаги
                updateSteps(2);
                
                // Обновляем цену
                updateTotal();
                
                showNotification(`Выбрана страна: ${data.name}`);
            }
            
            // Выбор опции
            function selectOption(option) {
                selectedOption = option;
                
                // Обновляем UI
                document.querySelectorAll('.option-item').forEach(item => {
                    item.classList.remove('selected');
                    if (item.dataset.option === option) {
                        item.classList.add('selected');
                    }
                });
                
                // Обновляем шаги
                updateSteps(3);
                
                // Обновляем цену
                updateTotal();
            }
            
            // Обновление шагов
            function updateSteps(activeStep) {
                document.querySelectorAll('.step').forEach((step, index) => {
                    if (index + 1 === activeStep) {
                        step.classList.add('active');
                    } else if (index + 1 < activeStep) {
                        step.classList.add('active');
                    } else {
                        step.classList.remove('active');
                    }
                });
            }
            
            // Обновление итоговой цены
            function updateTotal() {
                if (!selectedCountry) return;
                
                const basePrice = selectedCountry.price;
                const multiplier = options[selectedOption].multiplier;
                const total = (basePrice * multiplier).toFixed(2);
                
                document.getElementById('totalPrice').textContent = `$${total}`;
                document.getElementById('buyButton').textContent = `💳 Оплатить $${total}`;
                document.getElementById('buyButton').disabled = false;
            }
            
            // Обработка оплаты
            function processPayment() {
                if (!selectedCountry) {
                    showNotification('Пожалуйста, выберите страну!');
                    return;
                }
                
                const total = (selectedCountry.price * options[selectedOption].multiplier).toFixed(2);
                
                // Отправляем данные в Telegram бот
                tg.sendData(JSON.stringify({
                    action: 'create_invoice',
                    country: selectedCountry.name,
                    option: options[selectedOption].name,
                    price: total,
                    currency: 'USD'
                }));
                
                showNotification('Создание счета...');
                
                // В реальном приложении здесь будет вызов Crypto Bot API
                simulatePayment(total);
            }
            
            // Симуляция платежа (для демо)
            function simulatePayment(total) {
                showNotification(`Демо: Счет на $${total} создан!`);
                
                // В реальном приложении:
                // 1. Создание инвойса через Crypto Bot API
                // 2. Редирект на оплату
                // 3. Проверка статуса оплаты
                
                setTimeout(() => {
                    showNotification('✅ Оплата успешна! Данные аккаунта отправлены в бот.');
                }, 2000);
            }
            
            // Показать уведомление
            function showNotification(message) {
                const notification = document.getElementById('notification');
                notification.textContent = message;
                notification.style.display = 'block';
                
                setTimeout(() => {
                    notification.style.display = 'none';
                }, 3000);
            }
            
            // Инструкция
            function showInstructions() {
                tg.showAlert('Для покупки:\n1. Выберите страну\n2. Выберите опции\n3. Оплатите через Crypto Bot\n4. Получите данные в боте');
            }
            
            // Запуск при загрузке
            document.addEventListener('DOMContentLoaded', () => {
                loadCountries();
                
                // Обработка ответов от бота
                tg.onEvent('webAppDataReceived', (event) => {
                    console.log('Data from bot:', event.data);
                });
                
                // Инициализация
                tg.MainButton.setText('Готово к покупке!');
                tg.MainButton.show();
            });
        </script>
    </body>
    </html>
    """
    
    return web.Response(text=html, content_type='text/html')

async def handle_api(request):
    """API для создания инвойсов"""
    try:
        data = await request.json()
        
        # Здесь должен быть код для создания инвойса через Crypto Bot API
        # Используйте токен: 499354:AATdkiDyuC1tWd1ro5S5wFw6XcePNUNH5Ph
        
        return web.json_response({
            "success": True,
            "invoice_url": "https://t.me/CryptoBot?start=invoice_demo",
            "message": "Инвойс создан успешно"
        })
    except Exception as e:
        return web.json_response({
            "success": False,
            "error": str(e)
        }, status=400)

app = web.Application()
app.router.add_get('/', handle_mini_app)
app.router.add_post('/api/create_invoice', handle_api)

if __name__ == '__main__':
    web.run_app(app, port=3000, host='0.0.0.0')
