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
MODEL_DIR = "../weights/"
# LANGUAGE = "zh"

print("========================================")
print("Loading model into VRAM...")
print("========================================")
# Load models into VRAM here so they can be warm between requests
model = whisper.load_model("large-v2", device="cuda", download_root=MODEL_DIR)
print("========================================")
print("Model loaded successfully!")
print("========================================")

def handler(job):

    print(job)

    # grab all user input
    job_input = job['input']

    transcription=job_input.get('transcription', 'plain_text'),
    translate=job_input.get('translate', False),
    temperature=job_input.get('temperature', 0)
    language=job_input.get('language', None)

    # download audio file
    audio_file = download_files_from_urls(job['id'], job_input['audio'])[0]
    audio = whisper.load_audio(audio_file)    

    # generate transcription
    result = whisper.transcribe(
    model=model, 
    audio=audio,
    language=str(language),
    vad=True,
    compute_word_confidence=True,
    detect_disfluencies=True,
    # naive_approach=True,
    temperature=temperature,
    # no_speech_threshold=0.6,
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

    print(result)

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