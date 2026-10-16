from pathlib import Path
import json, wave, shutil
import config

## Copy voice samples that appear in the metadata from the raw data dir


def main():

  train_clean_360_dir = config.RAW_DATA_DIR / "libritts_r" / "train-clean-360"
  destination_dir = config.PROCESSED_DATA_DIR / "voice_samples"

  with open(config.PROCESSED_DATA_DIR / 'voice_metadata.json', 'r') as rfile:
    data: dict = json.load(rfile)

  for id, speaker in data.items():
    file_name = speaker["sample"]
    chapter = file_name.split('_')[1]
    file = train_clean_360_dir / id / chapter / file_name
    shutil.copy(file, destination_dir)


if __name__ == "__main__":
   main()