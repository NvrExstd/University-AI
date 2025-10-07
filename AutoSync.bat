@echo off
setlocal enabledelayedexpansion

rem Путь к корню репозитория
set REPO_ROOT=%cd%

rem Перейти в корень репозитория (если скрипт запускается из подкаталога)
cd /d "%REPO_ROOT%"

rem Обновить локальную копию с удаленного репозитория
git pull origin main

rem Проходим рекурсивно по всем папкам и добавляем все новые файлы
for /r "%REPO_ROOT%" %%f in (*) do (
    rem Добавить файлы в индекс
    git add "%%f"
)

rem Формируем сообщение коммита с датой и временем
for /f "tokens=2 delims==" %%a in ('wmic os get localdatetime /value ^| find "="') do set datetime=%%a
set datestamp=%datetime:~0,8%
set timestamp=%datetime:~8,6%
set commit_message=Auto sync %datestamp% %timestamp%

rem Сделать коммит с сообщением
git commit -m "%commit_message%"

rem Отправить изменения на удаленный репозиторий
git push origin main

