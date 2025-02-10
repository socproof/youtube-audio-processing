import whisper
import os
import torch
import time
from pyannote.audio import Pipeline
from threading import Thread, Event
from concurrent.futures import ThreadPoolExecutor
from whisper.utils import format_timestamp

from audio_processing.utils import diarize_text, write_to_txt, timer


def process_transcription_results(asr_result, resultpath1, resultpath2):
    """Processes and saves transcription results to files."""
    with open(resultpath1, "w", encoding="utf-8") as f1:
        for segment in asr_result['segments']:
            text = segment['text']
            f1.writelines(text + "\n======= {}:{}\n".format(segment['end'] // 60, segment['end'] % 60))

    with open(resultpath2, "w", encoding="utf-8") as f2:
        for segment in asr_result['segments']:
            start_time = format_timestamp(segment['start'], always_include_hours=True).split('.')[0]
            end_time = format_timestamp(segment['end'], always_include_hours=True).split('.')[0]
            text = f"[{start_time}-{end_time}] {segment['text']}"
            f2.writelines(text + '\n')


def process_speech(filepath, params):
    """Processes speech using Whisper and Pyannote in parallel."""
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
    resultpath1 = os.path.join(params['RESULTPATH'], '{}_net.txt'.format(name.rsplit('.', 1)[0]))
    resultpath2 = os.path.join(params['RESULTPATH'], '{}_net_ts.txt'.format(name.rsplit('.', 1)[0]))

    try:
        with ThreadPoolExecutor() as executor:
            diarization_future = executor.submit(run_diarization, filepath, params)
            transcription_future = executor.submit(asr_model.transcribe, filepath, **transcribe_options)

            diarization_result = diarization_future.result()
            asr_result = transcription_future.result()

            if diarization_result is None:
                raise RuntimeError("Diarization failed")
            if not asr_result.get('segments'):
                raise RuntimeError("Transcription failed")

        process_transcription_results(asr_result, resultpath1, resultpath2)

        final_result = diarize_text(asr_result, diarization_result)
        write_to_txt(final_result, resultpath.replace("_ts.txt", "_diarized.txt"))

    except Exception as e:
        print(f"Processing failed: {e}")
    finally:
        stop_event.set()
        t.join()

def run_diarization(filepath, params):
    """Performs diarization and returns the result."""
    print("\nStarting diarization...")
    start_time = time.time()
    try:
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=params['HF_TOKEN'])
        diarization_result = pipeline(filepath, num_speakers=params['NUM_SPEAKERS'])
        dt = (time.time() - start_time) / 60
        print("\nDiarization complete, it took {} minutes".format(round(dt, 2)))
        return diarization_result
    except Exception as e:
        print(f"Diarization error: {e}")
        return None