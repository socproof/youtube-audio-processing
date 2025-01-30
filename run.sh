#!/bin/bash

# Проверка, установлен ли Docker
if ! command -v docker &> /dev/null; then
    echo "Docker не установлен. Установите Docker и повторите попытку."
    exit 1
fi

# Проверка, установлен ли Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose не установлен. Установите Docker Compose и повторите попытку."
    exit 1
fi

# Проверка наличия GPU
echo "Проверка наличия GPU..."
if command -v nvidia-smi &> /dev/null; then
    echo "GPU обнаружен. Запуск с поддержкой GPU..."
    COMPOSE_FILES="-f docker-compose.yml -f docker-compose.gpu.yml"
else
    echo "GPU не обнаружен. Запуск без поддержки GPU..."
    COMPOSE_FILES="-f docker-compose.yml"
fi

# Сборка и запуск контейнера
echo "Запуск контейнера в фоновом режиме..."
docker-compose $COMPOSE_FILES up -d

if [ $? -ne 0 ]; then
    echo "Ошибка при сборке Docker-образа."
    exit 1
fi

# Получение имени (или ID) запущенного контейнера
CONTAINER_ID=$(docker-compose $COMPOSE_FILES ps -q app)

if [ -z "$CONTAINER_ID" ]; then
    echo "Контейнер с именем 'app' не найден. Проверьте docker-compose.yml и попробуйте снова."
    exit 1
fi

echo "Запуск Python-скрипта main.py внутри контейнера..."
docker exec -it "$CONTAINER_ID" python main.py

if [ $? -ne 0 ]; then
    echo "Ошибка при выполнении Python-скрипта внутри контейнера."
    exit 1
fi

echo "Контейнер успешно завершил работу."