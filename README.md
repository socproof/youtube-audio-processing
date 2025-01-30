# YouTube Audio Processing

## Описание

Этот проект позволяет загружать аудио из публичных видео на YouTube и выполнять его транскрипцию с возможностью разделения по спикерам (speaker diarization). Проект использует Docker для удобства развёртывания и работы.

---

## Что вам понадобится

1. **Установите Docker**:
   - Убедитесь, что Docker установлен на вашем компьютере. Если нет, скачайте и установите его с [официального сайта Docker](https://www.docker.com/).
   - Для ускорения обработки рекомендуется использовать видеокарту NVIDIA с поддержкой CUDA. Убедитесь, что драйверы NVIDIA и Docker с поддержкой GPU настроены:
      - [Linux](https://docs.docker.com/desktop/features/gpu/)
      - [Windows](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#configuration)

2. **Подготовка репозитория**:
   - Перейдите в директорию с репозиторием:
     ```bash
     cd /путь/к/папке/репозитория
     ```
   - Переименуйте файл `sample.params.yaml` в `params.yaml`:
     ```bash
     mv sample.params.yaml params.yaml
     ```

3. **Настройка Hugging Face**:
   - Перейдите на [Hugging Face](https://huggingface.co/) и выполните следующие шаги:
      1. Примите условия использования моделей:
         - [pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0)
         - [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)
      2. Создайте токен доступа на странице [hf.co/settings/tokens](https://huggingface.co/settings/tokens).
   - Укажите созданный токен в файле `params.yaml` в параметре `HF_TOKEN`.

4. **Дополнительные настройки**:
   - В файле `params.yaml` вы можете указать дополнительные параметры, например:
      - `NUM_SPEAKERS`: количество спикеров в видео (если известно заранее).
      - Другие параметры, специфичные для вашего проекта.

---

## Запуск проекта

1. **Подготовка к запуску**:
   - Если на вашей машине установлена видеокарта NVIDIA, убедитесь, что установлены **последние драйверы** и **Docker с поддержкой GPU**:
      - [Инструкция для Linux](https://docs.docker.com/desktop/features/gpu/)
      - [Инструкция для Windows](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#configuration)
   - Если видеокарта NVIDIA отсутствует, проект будет работать на процессоре, но обработка займет больше времени.

2. **Запуск проекта**:
   - В зависимости от вашей операционной системы выполните одну из следующих команд:
      - **Для Linux/macOS**:
        ```bash
        ./run.sh
        ```
      - **Для Windows**:
        ```bash
        run.bat
        ```
   - Эти скрипты автоматически определят, есть ли на вашей машине GPU, и запустят соответствующий конфигурационный файл `docker-compose`.

3. **Ввод данных**:
   - После запуска контейнера введите ссылку на видео с YouTube, которое нужно обработать.

4. **Обработка**:
   - В зависимости от мощности вашего компьютера и длины видео, обработка может занять от нескольких минут до нескольких часов.
   - Если у вас есть видеокарта NVIDIA, обработка будет значительно быстрее. В противном случае она будет выполняться на процессоре.
   
---

## Лицензия

Этот проект распространяется под лицензией [MIT](LICENSE).

---

Если у вас есть дополнительные вопросы или предложения, создайте issue в репозитории или свяжитесь с автором проекта.