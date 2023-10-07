import torch
import whisper_timestamped as whisper


# Load VAD model
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=True,
                              onnx=True)

# Load ASR model(s)
# model = whisper.load_model("tiny", device="cuda")
# model = whisper.load_model("base", device="cuda")
# model = whisper.load_model("small", device="cuda")
# model = whisper.load_model("medium", device="cuda")
# model = whisper.load_model("large-v1", device="cuda")
model = whisper.load_model("large-v2", device="cuda")