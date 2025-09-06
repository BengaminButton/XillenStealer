@echo off
echo 🚀 XillenStealer V3.0 - GitHub Updater
echo ================================================

echo 📋 Инициализация Git...
git init

echo 🔧 Настройка Git...
git config user.name "BengaminButton"
git config user.email "bengaminbutton@example.com"

echo 📝 Добавление всех изменений...
git add .

echo 🗑️ Удаление старых файлов...
git rm --cached "XillenStealer Builder.spec" 2>nul
git rm --cached "XillenStealer_Builder.spec" 2>nul
git rm --cached "README!!!!!.txt" 2>nul
git rm --cached "hook-tkinter.py.py" 2>nul
git rm --cached "XillenStealer Logo.jpg" 2>nul

echo 💾 Создание коммита...
git commit -m "🚀 XillenStealer V3.0 - Major Update

✨ New Features:
- Modern interface with animations
- Two themes: Deep Dark + Scarlet  
- VM Detection & Anti-Debug
- Process Injection & Persistence
- Game Launchers support
- Vivaldi Browser support
- Beautiful HTML reports
- Fixed all interface bugs

🛡️ Security:
- VM/Sandbox detection
- Process injection
- Task Scheduler persistence
- Anti-debug protection

🎮 Game Support:
- Epic Games Launcher
- Minecraft accounts
- GTA V data
- Enhanced Steam support

📊 UI/UX:
- Professional design
- Smooth animations
- Progress bars
- In-app notifications
- Responsive layout"

echo 🌐 Отправка на GitHub...
git remote add origin https://github.com/BengaminButton/XillenStealer.git
git branch -M main
git push -u origin main --force

echo ✅ Обновление завершено!
echo 🔗 Репозиторий: https://github.com/BengaminButton/XillenStealer
echo ⭐ XillenStealer V3.0 готов к использованию!

pause
