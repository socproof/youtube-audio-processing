@echo off
chcp 65001 >nul

:: Проверка, установлен ли Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker не установлен. Установите Docker и повторите попытку.
    exit /b 1
)

:: Проверка, установлен ли Docker Compose
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker Compose не установлен. Установите Docker Compose и повторите попытку.
    exit /b 1
)

:: Сборка Docker-образа
echo Сборка Docker-образа...
docker-compose build
if %errorlevel% neq 0 (
    echo Ошибка при сборке Docker-образа.
    exit /b 1
)

:: Запуск контейнера с интерактивным терминалом
echo Запуск контейнера с интерактивным терминалом...
docker-compose run --service-ports app sh
if %errorlevel% neq 0 (
    echo Ошибка при запуске контейнера.
    exit /b 1
)

echo Контейнер успешно завершил работу.
