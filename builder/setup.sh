#!/bin/bash

# Stop script on error
set -e

echo "#################### Updating and installing ffmpeg... ####################"
apt update -y && apt install -y ffmpeg
echo "#################### Installing whisper-timestamped... ####################"
pip3 install -q git+https://github.com/linto-ai/whisper-timestamped
echo "#################### Installing onnxruntime and torchaudio... ####################"
pip3 install -q onnxruntime torchaudio runpod
echo "#################### Setup completed. ####################"

