import config
import csv, re, json
from dataclasses import dataclass
from typing import Literal
from utils import get_wav_duration

@dataclass
class VoiceMetadata:
    name: str
    gender: Literal["F", "M"]
    piper_id: int
    sample: str
    pitch: str
    speaking_speed: str
    energy: str
    characteristics: list[str]
    


def main():

    # Load data from LibriTTS-R 'speakers.tsv' and create a set of libri_ids from the train-clean-360 set
    #   initialize output data dict with libri_ids as keys
    #   extract "gender" field from 'speakers.tsv'
    libri_ids = set() # Set of speaker ids from the train-clean-360 set
    output_data = dict()
    with open(config.RAW_DATA_DIR / "libritts_r/speakers.tsv", "r") as wfile:
        reader = csv.DictReader(wfile, delimiter='\t', fieldnames=["READER", "GENDER", "SUBSET", "NAME"])
        next(reader) # Skip over the header

        for row in reader: 
            if row["SUBSET"] == "train-clean-360":
                id = int(row["READER"])
                libri_ids.add(id)
                output_data[id] = {
                    "name": None,
                    "gender": row["GENDER"],
                    "piper_id": None,
                    "sample": None,
                    "pitch": None,
                    "speaking_speed": None,
                    "energy": None,
                    "characteristics": [],
                }

    # Load speaker data for train-clean-360 set from "ef#_en.csv" files into a dict with the "libri_id" as keys
    libri_p_spkr_data: list[dict] = []
    for file in (config.RAW_DATA_DIR / 'libritts_p').glob('*_en.csv'):
        with open(file, 'r') as rfile:
            df = {}
            reader = csv.DictReader(rfile, delimiter="|", fieldnames=["libri_id", "characteristics"])
            for row in reader:
                id = int(row["libri_id"])
                if id not in libri_ids:
                    continue

                characteristics: list[str] = row['characteristics'].split(',')
                simplified_characteristics = []

                # Simplify the characteristics by stripping quantifiers: "very", "slightly", and "-like"
                for characteristic in characteristics:
                    simplified = characteristic
                    simplified = re.sub('very ', '', simplified)
                    simplified = re.sub('slightly ', '', simplified)
                    simplified = re.sub('-like', '', simplified)
                    simplified_characteristics.append(simplified)

                df[id] = simplified_characteristics

        libri_p_spkr_data.append(df)

    # Exclude libri_ids that appear in the speaker anotations from Libritts-p, but are not in train-clean-360
    ids_to_remove = libri_ids.difference(df.keys())
    for id in ids_to_remove: 
        libri_ids.remove(id)
        del output_data[id]

    # Consolidate speaker characteristic annotations for all three annotators in LibriTTS-P in a combined dict
    combined_dict = dict()
    for id in libri_ids:
        combined_dict[id] = []
        for df in libri_p_spkr_data:
            combined_dict[id].extend(df[id])

    # Keep only characteristics that appear more than once for each key
    characteristics_set = set()
    for key in combined_dict:
        for characteristic in combined_dict[key]:
            if combined_dict[key].count(characteristic) > 1:
                if characteristic not in output_data[key]["characteristics"]:
                    output_data[key]["characteristics"].append(characteristic)
                    characteristics_set.add(characteristic)
    

    # Write intermediate output to a json file with speaker data for debugging
    with open(config.INTERMEDIATE_DATA_DIR / "libri_p_spkr_data.json", "w") as wfile:
        json.dump(output_data, wfile, indent=1)

    # Write characteristics set to file
    with open(config.PROCESSED_DATA_DIR / "characteristics.json", "w") as wfile:
            json.dump(sorted(list(characteristics_set)), wfile, indent=1)

    # Filter wav file names for only files whose libri_id is in the dataset, where the file has annotations from libritts-p
    #  and the audio is between 6 - 10 seconds in duration,
    filtered_files = []
    wav_files_path = (config.RAW_DATA_DIR / 'libritts_r' / 'train-clean-360')
    annotated_wav_files: list[dict] = [] # TODO: Make this a list of id object (file: Path, [])
    with open(config.RAW_DATA_DIR / "libritts_p/metadata_w_style_prompt_tags_v230922.csv", "r") as rfile:
        reader = csv.DictReader(rfile)
        for row in reader: 
            id = row["spk_id"]

            if int(id) not in libri_ids:
                continue

            file_idx = row["item_name"].split("_")[1]
            file = wav_files_path / id / file_idx / (row["item_name"] + ".wav")
            annotated_wav_files.append({
                "file": file,
                "pitch": row["pitch"],
                "speaking_speed": row["speaking_speed"],
                "energy": row["energy"],
            })

    # Extract sample name, pitch and speaking speed, replacing 'very' 
    for id in libri_ids:
        for entry in annotated_wav_files: 
            if id == int(entry["file"].name.split('_')[0]):
                if get_wav_duration(entry["file"]) in range(5, 10):
                    filtered_files.append(entry)
                    output_data[id]["sample"] = entry["file"].name
                    output_data[id]["pitch"] = re.sub("very ", "", entry["pitch"])
                    output_data[id]["speaking_speed"] = re.sub("very ", "", entry["speaking_speed"])
                    output_data[id]["energy"] = re.sub("very ", "", entry["energy"])

    # Remove entries from output data for which no sample was found
    ids_to_remove = []
    for id, speaker in output_data.items():
        if not speaker["sample"]:
            ids_to_remove.append(id)

    for id in ids_to_remove:
        del output_data[id]
        libri_ids.remove(id)

    # Write intermediate output to a json file for debugging
    with open(config.INTERMEDIATE_DATA_DIR / "libri_p_spkr_data.json", "w") as wfile:
        json.dump(output_data, wfile, indent=1)    

    # Add piper ids from en_US-libritts_r-medium
    with open(config.RAW_DATA_DIR / "piper" / "en_US-libritts_r-medium.onnx.json", "r") as rfile: 
        piper_data = json.load(rfile)
        speaker_id_map = piper_data["speaker_id_map"]
        for id in speaker_id_map.keys():
            if int(id) in libri_ids:
                output_data[int(id)]["piper_id"] = speaker_id_map[id]

    
    # Write intermediate output to a json file for debugging
    with open(config.INTERMEDIATE_DATA_DIR / "libri_p_spkr_data.json", "w") as wfile:
        json.dump(output_data, wfile, indent=1)   

    # Load names from intermediate data
    with open(config.INTERMEDIATE_DATA_DIR / "names.json", "r") as rfile:
        names = json.load(rfile)

        for _id, speaker in output_data.items():
            # Male names
            if (speaker["gender"] == "M"):
                if ("adult" in speaker["characteristics"]):
                    speaker["name"] = names["adult_m_names"].pop()
                elif ("young" in speaker["characteristics"]):
                    speaker["name"] = names["young_m_names"].pop()
                elif ("middle-aged" in speaker["characteristics"]):
                    speaker["name"] = names["middle_aged_m_names"].pop()
                elif ("old" in speaker["characteristics"]):
                    speaker["name"] = names["old_m_names"].pop()
                else:
                    speaker["name"] = names["no_age_m_names"].pop()
            # Female names
            if (speaker["gender"] == "F"):
                if ("adult" in speaker["characteristics"]):
                    speaker["name"] = names["adult_f_names"].pop()
                elif ("young" in speaker["characteristics"]):
                    speaker["name"] = names["young_f_names"].pop()
                elif ("middle-aged" in speaker["characteristics"]):
                    speaker["name"] = names["middle_aged_f_names"].pop()
                elif ("old" in speaker["characteristics"]):
                    speaker["name"] = names["old_f_names"].pop()
                else:
                    speaker["name"] = names["no_age_f_names"].pop()

    with open(config.PROCESSED_DATA_DIR / "voice_metadata.json", "w") as wfile: 
        json.dump(output_data, wfile, indent=1)

if __name__ == "__main__":
    main()