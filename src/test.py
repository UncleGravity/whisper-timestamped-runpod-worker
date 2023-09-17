import os
import json
import whisper_timestamped as whisper
from make_subtitles import write_srt, write_vtt

AUDIO_FILE = "./input/yt-audio-adbb0e15-e2e2-4b7c-8cc7-be6653bc1d0e.mp3"
MODEL_DIR = "./models/"
LANGUAGE = "zh"

audio = whisper.load_audio(AUDIO_FILE)
model = whisper.load_model("large-v2", device="cuda", download_root=MODEL_DIR)
result = whisper.transcribe(
    model=model, 
    audio=audio, 
    language=LANGUAGE, 
    vad=True,
    compute_word_confidence=True,
    detect_disfluencies=True,
    # naive_approach=True,
    temperature=.4,
    # no_speech_threshold=0.6,
    verbose=True,
    )

# Save the result as a JSON file
with open('result.json', 'w') as f:
    json.dump(result, f, ensure_ascii=False)

# Convert the JSON file to SRT and VTT files
input_file = 'result.json'
output_files = ['result.srt', 'result.vtt']

with open(input_file, "r", encoding="utf-8") as f:
    transcript = json.load(f)
segments = transcript["segments"]

# Write to SRT and VTT files
for output in output_files:
    if output.endswith(".srt"):
        with open(output, "w", encoding="utf-8") as f:
            write_srt(segments, file=f)
    elif output.endswith(".vtt"):
        with open(output, "w", encoding="utf-8") as f:
            write_vtt(segments, file=f)
    else:
        raise RuntimeError(f"Unknown output format for {output}")