from datasets import load_dataset, Audio
import os
import shutil
from tqdm import tqdm

OUT_DIR = "zhongli_en"
os.makedirs(OUT_DIR, exist_ok=True)

dataset = load_dataset(
    "simon3000/genshin-voice",
    split="train",
    streaming=True
).cast_column("audio", Audio(decode=False))

meta = []

idx = 0
for sample in tqdm(dataset, desc="Extracting Zhongli EN"):
    if sample.get("speaker") != "Zhongli":
        continue
    if sample.get("language") != "English(US)":
        continue

    audio_path = sample["audio"]["path"]
    text = sample["text"].strip()

    filename = f"zhongli_{idx:05d}.wav"
    dst = os.path.join(OUT_DIR, filename)

    shutil.copy(audio_path, dst)
    meta.append(f"{filename}|{text}")
    idx += 1

with open(os.path.join(OUT_DIR, "metadata.csv"), "w", encoding="utf-8") as f:
    f.write("\n".join(meta))
