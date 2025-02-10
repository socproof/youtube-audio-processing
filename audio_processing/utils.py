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

        if text and text[-1] in PUNC_SENT_END:
            merged_spk_text.append(merge_cache(text_cache))
            text_cache = []
            current_speaker = None

    if text_cache:
        merged_spk_text.append(merge_cache(text_cache))

    return merged_spk_text

def merge_consecutive_speaker_segments(diarized_segments):
    """Combines consecutive lines of one speaker."""
    merged_segments = []
    current_segment = None

    for segment in diarized_segments:
        if current_segment is None:
            current_segment = segment
        elif current_segment['speaker'] == segment['speaker']:
            current_segment['end'] = segment['end']
            current_segment['text'] += " " + segment['text']
        else:
            merged_segments.append(current_segment)
            current_segment = segment

    if current_segment is not None:
        merged_segments.append(current_segment)

    return merged_segments

def diarize_text(transcribe_res, diarization_result):
    """Combines transcription and diarization results."""
    timestamp_texts = get_text_with_timestamp(transcribe_res)
    spk_text = add_speaker_info_to_text(timestamp_texts, diarization_result)
    merged_spk_text = merge_sentence(spk_text)

    diarized_segments = []
    for seg, speaker, sentence in merged_spk_text:
        diarized_segments.append({
            'start': seg.start,
            'end': seg.end,
            'speaker': speaker,
            'text': sentence
        })

    merged_segments = merge_consecutive_speaker_segments(diarized_segments)

    return merged_segments

def write_to_txt(spk_sent, file):
    """Saves the merged replicas to a file."""
    with open(file, 'w', encoding="utf-8") as fp:
        for segment in spk_sent:
            start_time = segment['start']
            end_time = segment['end']
            speaker = segment['speaker']
            text = segment['text']
            fp.write(f'{start_time:.2f} {end_time:.2f} {speaker} {text}\n')
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
