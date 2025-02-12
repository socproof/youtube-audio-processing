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

:: Проверка наличия GPU
echo Проверка наличия GPU...
nvidia-smi >nul 2>&1
if %errorlevel% equ 0 (
    echo GPU обнаружен. Запуск с поддержкой GPU...
    set COMPOSE_FILES=-f docker-compose.yml -f docker-compose.gpu.yml
) else (
    echo GPU не обнаружен. Запуск без поддержки GPU...
    set COMPOSE_FILES=-f docker-compose.yml
)

:: Запуск контейнера в фоновом режиме
echo Запуск контейнера в фоновом режиме...
docker-compose %COMPOSE_FILES% up -d
if %errorlevel% neq 0 (
    echo Ошибка при запуске контейнера.
    exit /b 1
)

:: Получение имени (или ID) запущенного контейнера
for /f "tokens=*" %%i in ('docker-compose %COMPOSE_FILES% ps -q app') do set CONTAINER_ID=%%i

:: Проверка, удалось ли получить контейнер
if "%CONTAINER_ID%"=="" (
    echo Контейнер с именем "app" не найден. Проверьте docker-compose.yml и попробуйте снова.
    exit /b 1
)

:: Запуск Python-скрипта внутри контейнера
echo Запуск Python-скрипта main.py внутри контейнера...
docker exec -it %CONTAINER_ID% python main.py
if %errorlevel% neq 0 (
    echo Ошибка при выполнении Python-скрипта внутри контейнера.
    exit /b 1
)

echo Контейнер успешно завершил работу.