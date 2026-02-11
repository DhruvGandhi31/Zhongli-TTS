import os
import shutil
import numpy as np
import soundfile as sf

BASE_DIR = "./data"
SOURCE_DIR = os.path.join(BASE_DIR, "zhongli_en")
BAD_DIR = os.path.join(BASE_DIR, "bad_data")

MIN_DURATION = 0.5        # seconds
SILENCE_THRESHOLD = 1e-4  # amplitude threshold
# ------------------------

# os.makedirs(BAD_DIR, exist_ok=True)

def is_corrupted_or_silent(wav_path):
    try:
        audio, sr = sf.read(wav_path)

        # If stereo, convert to mono
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)

        duration = len(audio) / sr

        if duration < MIN_DURATION:
            return True, f"Too short ({duration:.2f}s)"

        if len(audio) == 0:
            return True, "Zero length"

        max_amplitude = np.max(np.abs(audio))

        if max_amplitude < SILENCE_THRESHOLD:
            return True, "Silent / near zero amplitude"

        return False, "OK"

    except Exception as e:
        return True, f"Corrupted ({str(e)})"


def move_pair(base_name):
    wav_file = base_name + ".wav"
    txt_file = base_name + ".txt"

    wav_src = os.path.join(SOURCE_DIR, wav_file)
    txt_src = os.path.join(SOURCE_DIR, txt_file)

    wav_dst = os.path.join(BAD_DIR, wav_file)
    txt_dst = os.path.join(BAD_DIR, txt_file)

    if os.path.exists(wav_src):
        shutil.move(wav_src, wav_dst)

    if os.path.exists(txt_src):
        shutil.move(txt_src, txt_dst)


def main():
    total = 0
    rejected = 0

    for file in os.listdir(SOURCE_DIR):
        if file.endswith(".wav"):
            total += 1
            base_name = os.path.splitext(file)[0]
            wav_path = os.path.join(SOURCE_DIR, file)

            is_bad, reason = is_corrupted_or_silent(wav_path)

            if is_bad:
                print(f"[REJECTED] {file} -> {reason}")
                move_pair(base_name)
                rejected += 1
            else:
                print(f"[OK] {file}")

    print("\nFinished.")
    print(f"Total checked: {total}")
    print(f"Rejected: {rejected}")
    print(f"Kept: {total - rejected}")


if __name__ == "__main__":
    main()
