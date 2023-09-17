FROM runpod/pytorch:3.10-2.0.0-117

SHELL ["/bin/bash", "-c"]

WORKDIR /

# Update and upgrade the system packages (Worker Template)
RUN apt-get update && \
    apt-get upgrade -y

# Install System Packages
RUN apt-get install ffmpeg -y

# Run setup script instead of doing things on Dockerfile
# COPY builder/setup.sh /setup.sh
# RUN /bin/bash /setup.sh && \
#     rm /setup.sh


# Install Python dependencies (Worker Template)
RUN pip3 install -q git+https://github.com/linto-ai/whisper-timestamped
RUN pip3 install -q onnxruntime torchaudio runpod
# COPY builder/requirements.txt /requirements.txt
# RUN pip install --upgrade pip && \
#     pip install -r /requirements.txt && \
#     rm /requirements.txt

# Download Models
COPY builder/download_models.sh /download_models.sh
RUN chmod +x /download_models.sh && \
    /download_models.sh
RUN rm /download_models.sh

ADD src .

# Cleanup section (Worker Template)
RUN apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

CMD [ "python", "-u", "/handler.py" ]