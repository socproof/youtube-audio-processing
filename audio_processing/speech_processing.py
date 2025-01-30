import whisper
import os
import torch
import time
from pyannote.audio import Pipeline
from threading import Thread, Event
from concurrent.futures import ThreadPoolExecutor

from audio_processing.utils import diarize_text, write_to_txt, timer, split_audio, process_chunk


def process_speech(filepath, params):
    """
    Transcribes audio files using Whisper and performs speaker diarization using Pyannote.

    Args:
        filepath (str): Path to the audio file.
        params (dict): Parameters for transcription and diarization.
    """

    os.makedirs(params['RESULTPATH'], exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    print(f"Processing file: {filepath}")

    stop_event = Event()
    t = Thread(target=timer, args=(stop_event,))
    t.start()

    asr_model = whisper.load_model(name=params['MODEL_NAME'], device=device, download_root='assets/models')
    transcribe_options = dict(task="transcribe", language=params['LANG'])

    name = os.path.basename(filepath)
    resultpath = os.path.join(params['RESULTPATH'], '{}_ts.txt'.format(name.rsplit('.', 1)[0]))

    try:
        # Запускаем диаризацию в отдельном потоке
        diarization_thread = Thread(target=run_diarization, args=(filepath, params))
        diarization_thread.start()

        # Разделяем аудио на чанки
        chunks = split_audio(filepath)

        # Обрабатываем чанки параллельно
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_chunk, asr_model, chunk, transcribe_options) for chunk in chunks]
            asr_results = [future.result() for future in futures]

        # Объединяем результаты распознавания
        asr_result = {"segments": []}
        for result in asr_results:
            asr_result["segments"].extend(result["segments"])

        diarization_thread.join()

        final_result = diarize_text(asr_result, diarization_result)
        write_to_txt(final_result, resultpath)

    except Exception as e:
        print(f"Processing failed: {e}")
    finally:
        stop_event.set()
        t.join()

def run_diarization(filepath, params):
    """Performs diarization."""
    global diarization_result
    print("\nStarting diarization...")
    start_time = time.time()
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=params['HF_TOKEN'])
    diarization_result = pipeline(filepath, num_speakers=params['NUM_SPEAKERS'])
    dt = (time.time() - start_time) / 60
    print("\nDiarization complete, it took {} minutes".format(round(dt, 2)))