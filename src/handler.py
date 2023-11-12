#!/usr/bin/env python
''' Contains the handler function that will be called by the serverless. '''
import runpod
# from runpod.serverless.utils.rp_validator import validate
from runpod.serverless.utils import download_files_from_urls, rp_cleanup
from whisper.tokenizer import LANGUAGES
from whisper.utils import format_timestamp
import whisper_timestamped as whisper
from make_subtitles import write_srt, write_vtt
import os
import json

# AUDIO_FILE = "./input/yt-audio-adbb0e15-e2e2-4b7c-8cc7-be6653bc1d0e.mp3"
MODEL_DIR = "./weights/"
# LANGUAGE = "zh"

print("Starting serverless function")
print("========================================")
print("Loading model into VRAM...")
print("========================================")
# Load models into VRAM here so they can be warm between requests
model = whisper.load_model("large-v3", device="cuda", download_root=MODEL_DIR)
print("========================================")
print("Model loaded successfully!")
print("========================================")

def handler(job):

    print(job)

    # grab all user input
    job_input = job['input']

    transcription=job_input.get('transcription', 'plain_text'),
    translate=job_input.get('translate', False),

    # download audio file
    audio_file = download_files_from_urls(job['id'], job_input['audio'])[0]
    audio = whisper.load_audio(audio_file)    

    # generate transcription
    result = whisper.transcribe(
    model=model, 
    audio=whisper.load_audio(audio_file),
    language=job_input.get('language', None),
    vad=True,
    compute_word_confidence=True,
    detect_disfluencies=True,
    # naive_approach=True,
    temperature=job_input.get('temperature', 0),
    task=job_input.get('task', "transcribe"),
    beam_size=job_input.get('beam_size', 0),
    patience=job_input.get('patience', 0),
    best_of=job_input.get('best_of', 0),
    initial_prompt=job_input.get('initial_prompt', None),
    no_speech_threshold=job_input.get('no_speech_threshold', 0.6),
    # verbose=True,
    )

    # parse transcription
    if transcription == "plain text":
        transcription = result["text"]
    elif transcription == "srt":
        transcription = write_srt(result["segments"])
    else:
        transcription = write_vtt(result["segments"])

    # generate translation
    # if translate:
    #     translation = model.transcribe(
    #         str(audio), task="translate", temperature=temperature, **args
    #     )
    # else:
    #     translation = {"text": None}

    # print(result)
    with open('result.json', 'w') as f:
        json.dump(result, f)

    return {
        "segments": result["segments"],
        "detected_language": LANGUAGES[result["language"]],
        "transcription": transcription,
        # "translation": translation["text"] if translate else None,
        "translation": None,
    }

    # return json.dumps(result)



def write_vtt(transcript):
    '''
    Write the transcript in VTT format.
    '''
    result = ""
    for segment in transcript:
        result += f"{format_timestamp(segment['start'])} --> {format_timestamp(segment['end'])}\n"
        result += f"{segment['text'].strip().replace('-->', '->')}\n"
        result += "\n"
    return result


def write_srt(transcript):
    '''
    Write the transcript in SRT format.
    '''
    result = ""
    for i, segment in enumerate(transcript, start=1):
        result += f"{i}\n"
        result += f"{format_timestamp(segment['start'], always_include_hours=True, decimal_marker=',')} --> "
        result += f"{format_timestamp(segment['end'], always_include_hours=True, decimal_marker=',')}\n"
        result += f"{segment['text'].strip().replace('-->', '->')}\n"
        result += "\n"
    return result


runpod.serverless.start({"handler": handler})