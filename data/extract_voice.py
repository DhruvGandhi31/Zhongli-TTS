from datasets import load_dataset, Audio
import os
import shutil
import soundfile as sf

OUT_DIR = "zhongli_en"
os.makedirs(OUT_DIR, exist_ok=True)

dataset = load_dataset(
    "simon3000/genshin-voice",
    split="train",
    streaming=True
)

dataset = dataset.cast_column("audio", Audio(decode=False))

en_zhongli_dataset = dataset.filter(lambda x: x.get("speaker") == "Zhongli" and x.get("language") == "English(US)")

idx = 0
for i, voice in enumerate(en_zhongli_dataset):
    audio_dst = os.path.join(OUT_DIR, f"zhongli_{i:05d}.wav")
    text_dst = os.path.join(OUT_DIR, f"zhongli_{i:05d}.txt")

    audio_bytes = voice["audio"]["bytes"]

    # Write WAV bytes directly (no decoding, no re-encoding)
    with open(audio_dst, "wb") as f:
        f.write(audio_bytes)

    with open(text_dst, "w", encoding="utf-8") as f:
        f.write(voice["transcription"].strip())
    idx += 1
    print(idx)
