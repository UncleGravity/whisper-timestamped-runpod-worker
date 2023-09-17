#!/usr/bin/env python
''' Contains the handler function that will be called by the serverless. '''
import runpod
# from runpod.serverless.utils.rp_validator import validate
from runpod.serverless.utils import download_files_from_urls, rp_cleanup
import whisper_timestamped as whisper
from make_subtitles import write_srt, write_vtt
import os
import json

# AUDIO_FILE = "./input/yt-audio-adbb0e15-e2e2-4b7c-8cc7-be6653bc1d0e.mp3"
MODEL_DIR = "./weights/"
# LANGUAGE = "zh"

# Load models into VRAM here so they can be warm between requests
model = whisper.load_model("large-v2", device="cuda", download_root=MODEL_DIR)

def handler(job):

    print(job)
    job_input = job['input']

    # download audio file
    audio_file = download_files_from_urls(job['id'], job_input['audio'])[0]
    audio = whisper.load_audio(audio_file)    

    # do the things
    result = whisper.transcribe(
    model=model, 
    audio=audio,
    language=job_input['language'],
    vad=True,
    compute_word_confidence=True,
    detect_disfluencies=True,
    # naive_approach=True,
    temperature=.4,
    # no_speech_threshold=0.6,
    # verbose=True,
    )

    # return the output that you want to be returned like pre-signed URLs to output artifacts
    return json.dumps(result)


runpod.serverless.start({"handler": handler})