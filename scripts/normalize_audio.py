import os
import shutil
import numpy as np
import soundfile as sf
import librosa

SOURCE_DIR = "data/zhongli_en"
TARGET_DIR = "data/clean_v1"

TARGET_SR = 22050
TARGET_RMS = 0.1  # simple loudness normalization

os.makedirs(TARGET_DIR, exist_ok=True)

def normalize_rms(audio, target_rms=0.1):
    rms = np.sqrt(np.mean(audio**2))
    if rms > 0:
        audio = audio * (target_rms / rms)
    return audio

def process_file(base_name):
    wav_path = os.path.join(SOURCE_DIR, base_name + ".wav")
    txt_path = os.path.join(SOURCE_DIR, base_name + ".txt")

    try:
        audio, sr = sf.read(wav_path)

        # Convert to mono
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)

        # Resample
        if sr != TARGET_SR:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=TARGET_SR)

        # Normalize loudness
        audio = normalize_rms(audio, TARGET_RMS)

        # Save cleaned audio
        sf.write(
            os.path.join(TARGET_DIR, base_name + ".wav"),
            audio,
            TARGET_SR
        )

        # Copy transcript
        if os.path.exists(txt_path):
            shutil.copy(txt_path, os.path.join(TARGET_DIR, base_name + ".txt"))

        return True

    except Exception as e:
        print(f"Failed: {base_name} | {e}")
        return False


def main():
    count = 0

    for file in os.listdir(SOURCE_DIR):
        if file.endswith(".wav"):
            base_name = os.path.splitext(file)[0]
            if process_file(base_name):
                count += 1

    print(f"Processed {count} files.")


if __name__ == "__main__":
    main()
