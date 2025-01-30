#!/bin/bash

export LANG=ru_RU.UTF-8
export LC_ALL=ru_RU.UTF-8

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

# Сборка и запуск контейнера
echo "Сборка Docker-образа..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "Ошибка при сборке Docker-образа."
    exit 1
fi

echo "Запуск контейнера с интерактивным терминалом..."
docker-compose run --service-ports app

if [ $? -ne 0 ]; then
    echo "Ошибка при запуске контейнера."
    exit 1
fi

echo "Контейнер успешно завершил работу."
