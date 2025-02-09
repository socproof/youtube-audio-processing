import sys
import time

from pyannote.core import Segment

PUNC_SENT_END = {'.', '?', '!'}  # Using a set for faster lookups

def get_text_with_timestamp(transcribe_res):
    """Extracts text segments with timestamps from transcription results."""
    return [(Segment(item['start'], item['end']), item['text']) for item in transcribe_res['segments']]

def add_speaker_info_to_text(timestamp_texts, diarization_result):
    """Adds speaker information to text segments using diarization results."""
    return [(seg, diarization_result.crop(seg).argmax(), text) for seg, text in timestamp_texts]

def merge_cache(text_cache):
    """Merges cached text segments for the same speaker into a single segment."""
    start = text_cache[0][0].start
    end = text_cache[-1][0].end
    speaker = text_cache[0][1]
    sentence = ''.join(item[2] for item in text_cache)
    return Segment(start, end), speaker, sentence

def merge_sentence(spk_text):
    """Merges text segments into sentences based on punctuation and speaker changes."""
    merged_spk_text = []
    text_cache = []
    current_speaker = None

    for seg, speaker, text in spk_text:
        if current_speaker is not None and speaker != current_speaker:
            merged_spk_text.append(merge_cache(text_cache))
            text_cache = []

        text_cache.append((seg, speaker, text))
        current_speaker = speaker

        if text and text[-1] in PUNC_SENT_END:  # Check if text is not empty
            merged_spk_text.append(merge_cache(text_cache))
            text_cache = []
            current_speaker = None  # Reset speaker after sentence end

    if text_cache:  # Handle remaining segments
        merged_spk_text.append(merge_cache(text_cache))

    return merged_spk_text

def diarize_text(transcribe_res, diarization_result):
    """Combines transcription and diarization results into a single output."""
    timestamp_texts = get_text_with_timestamp(transcribe_res)
    spk_text = add_speaker_info_to_text(timestamp_texts, diarization_result)
    return merge_sentence(spk_text)

def write_to_txt(spk_sent, file):
    """Writes diarized sentences with timestamps and speaker information to a text file."""
    with open(file, 'w', encoding="utf-8") as fp:
        for seg, spk, sentence in spk_sent:
            fp.write(f'{seg.start:.2f} {seg.end:.2f} {spk} {sentence}\n')
        print(f'File has been written to {file}')

def timer(stop_event):
    """A simple timer that prints elapsed time until the stop_event is set."""
    seconds = 0
    sys.stdout.write("\n")
    while not stop_event.is_set():
        sys.stdout.write(f"\r{seconds} seconds passed...")
        sys.stdout.flush()
        seconds += 1
        time.sleep(1)
    sys.stdout.write("\nTimer stopped.\n")
