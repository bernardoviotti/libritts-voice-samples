import json
from pathlib import Path
import config

male_speakers = []
female_speakers = []
young_m = []
young_f = []
adult_m = []
adult_f = []
middle_aged_m = []
middle_aged_f = []
old_m = []
old_f = []
no_age_m = []
no_age_f = []


with open(config.INTERMEDIATE_DATA_DIR / "libri_p_spkr_data.json", "r") as rfile:
    data = json.load(rfile)

    for id, speaker in data.items():
        # Female speakers
        if speaker["gender"] == "F": 
            female_speakers.append({id: speaker})
            if "adult" in speaker["characteristics"]:
                adult_f.append({id: speaker})
            elif "young" in speaker["characteristics"]:
                young_f.append({id: speaker})
            elif "middle-aged" in speaker["characteristics"]:
                middle_aged_f.append({id: speaker})
            elif "old" in speaker["characteristics"]:
                old_f.append({id: speaker})
            else:
                no_age_f.append({id: speaker})

        # Male speakers
        else:
            male_speakers.append({id: speaker})
            if "adult" in speaker["characteristics"]:
                adult_m.append({id: speaker})
            elif "young" in speaker["characteristics"]:
                young_m.append({id: speaker})
            elif "middle-aged" in speaker["characteristics"]:
                middle_aged_m.append({id: speaker})
            elif "old" in speaker["characteristics"]:
                old_m.append({id: speaker})
            else:
                no_age_m.append({id: speaker})

    print("total=", len(data.keys()))
    print("male_speakers=", len(male_speakers))
    print("female_speakers=", len(female_speakers))
    print("young_m=", len(young_m))
    print("young_f=", len(young_f))
    print("adult_m=", len(adult_m))
    print("adult_f=", len(adult_f))
    print("middle_aged_m=", len(middle_aged_m))
    print("middle_aged_f=", len(middle_aged_f))
    print("old_f=", len(old_f))
    print("old_m=", len(old_m))
    print("no_age_m=", len(no_age_m))
    print("no_age_f=", len(no_age_f))
