import os
import re

DATA_DIR = "data/clean_v1"
METADATA_PATH = os.path.join(DATA_DIR, "metadata.csv")

def clean_text(text):
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('"', '')
    return text

def main():
    entries = []

    for file in os.listdir(DATA_DIR):
        if file.endswith(".wav"):
            base = os.path.splitext(file)[0]
            txt_path = os.path.join(DATA_DIR, base + ".txt")

            if not os.path.exists(txt_path):
                continue

            with open(txt_path, "r", encoding="utf-8") as f:
                text = clean_text(f.read())

            if len(text) == 0:
                continue

            entries.append(f"{file}|{text}")

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        for line in entries:
            f.write(line + "\n")

    print(f"Metadata built with {len(entries)} entries.")


if __name__ == "__main__":
    main()
