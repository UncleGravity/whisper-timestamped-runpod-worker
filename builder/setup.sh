#!/bin/bash

# Stop script on error
set -e

echo "#################### Updating and installing ffmpeg... ####################"
apt update -y && apt install -y ffmpeg
echo "#################### Installing whisper-timestamped... ####################"
pip3 install -q git+https://github.com/linto-ai/whisper-timestamped
echo "#################### Installing onnxruntime and torchaudio... ####################"
pip3 install -q onnxruntime torchaudio runpod
echo "#################### Installing VAD models "####################"
python fetch_vad_model.py
echo "#################### Installing ASR models "####################"
chmod +x ./fetch_asr_models.sh
./fetch_asr_models.sh
echo "#################### Setup completed. ####################"

