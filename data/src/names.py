import config
from pathlib import Path
import json, csv

# TARGETS:
## Speaker counts
# young_m_num_spkrs = 0
young_f_num_spkrs = 33
adult_m_num_spkrs = 248
adult_f_num_spkrs = 275
middle_aged_m_num_spkrs = 61
middle_aged_f_num_spkrs = 46
# old_f_num_spkrs = 0
old_m_num_spkrs = 11
no_age_m_num_spkrs = 13
no_age_f_num_spkrs = 1

def main() -> None:
    pop_cutoff = 1000
    output_names = {
        "old_m_names": [],
        # "old_f_names": list(old_f_names),
        "middle_aged_m_names": [],
        "middle_aged_f_names": [],
        "adult_m_names": [],
        "adult_f_names": [],
        # "young_m_names": list(young_m_names),
        "young_f_names": [],
        "no_age_m_names": [],
        "no_age_f_names": [],
    }

    while(
        len(output_names["young_f_names"]) < young_f_num_spkrs
        or len(output_names["adult_m_names"]) < adult_m_num_spkrs
        or len(output_names["adult_f_names"]) < adult_f_num_spkrs
        or len(output_names["middle_aged_m_names"]) < middle_aged_m_num_spkrs
        or len(output_names["middle_aged_f_names"]) < middle_aged_f_num_spkrs
        or len(output_names["old_m_names"]) < old_m_num_spkrs
    ):
        output_names = get_names(pop_cutoff)
        pop_cutoff -= 100

    print("pop_cutoff=", pop_cutoff)
    print("old_m_names=", len(output_names["old_m_names"]))
    print("middle_aged_m_names=", len(output_names["middle_aged_m_names"]))
    print("middle_aged_f_names=", len(output_names["middle_aged_f_names"]))
    print("adult_m_names=", len(output_names["adult_m_names"]))
    print("adult_f_names=", len(output_names["adult_f_names"]))
    print("young_f_names=", len(output_names["young_f_names"]))
    

    with open(config.INTERMEDIATE_DATA_DIR / "names.json", "w") as wfile:
            json.dump(output_names, wfile, indent=1)


def get_names(pop_cutoff) -> dict[str, list]:

    # Extract names from SSA data into sets broken down by birth age
    all_names = set()

  

    old_m_names = set() # Set of male baby names born between 1960 - 1972 that meet the pop cutoff
    middle_aged_m_names = set() #  ... between 1973 - 1985
    middle_aged_f_names = set() # ...  between 1973 - 1985
    adult_m_names = set() # ... between 1986 - 2000
    adult_f_names = set() # ... between 1986 - 2000
    young_f_names = set() # ... between 2001 - 2010
    no_age_m_names = set()
    no_age_f_names = set()

    old_range = range(1960, 1973)
    middle_aged_range = range(1973, 1986)
    adult_range = range(1986, 2001)
    young_range = range(2001, 2010)

    for year in adult_range:
        with open(config.RAW_DATA_DIR / "names" / f"yob{year}.txt", "r") as rfile:
            reader = csv.DictReader(rfile, fieldnames=["name", "gender", "pop"])
            next(reader) # Skip the header

            for row in reader: 
                # Ignore names below the pop cutoff
                if int(row["pop"]) < pop_cutoff:
                    continue

                # Ignore non unique names
                elif row["name"] in all_names:
                    continue

                all_names.add(row["name"])

                if row["gender"] == "F":
                    if len(adult_f_names) >= adult_f_num_spkrs:
                        continue
                    adult_f_names.add(row["name"])
                else:
                    if len(adult_m_names) >= adult_m_num_spkrs:
                        continue
                    adult_m_names.add(row["name"])



    for year in middle_aged_range:
        with open(config.RAW_DATA_DIR / "names" / f"yob{year}.txt", "r") as rfile:
            reader = csv.DictReader(rfile, fieldnames=["name", "gender", "pop"])
            next(reader) # Skip the header

            for row in reader: 
                # Ignore names below the pop cutoff
                if int(row["pop"]) < pop_cutoff:
                    continue

                # Ignore non unique names
                elif row["name"] in all_names:
                    continue


                if row["gender"] == "M":
                    if len(middle_aged_m_names) >= middle_aged_m_num_spkrs:
                        continue
                    middle_aged_m_names.add(row["name"])
                    all_names.add(row["name"])

                elif row["gender"] == "F":
                    if len(middle_aged_f_names) >= middle_aged_f_num_spkrs:
                        continue
                    middle_aged_f_names.add(row["name"])
                    all_names.add(row["name"])                    


        
    for year in young_range:
            with open(config.RAW_DATA_DIR / "names" / f"yob{year}.txt", "r") as rfile:
                reader = csv.DictReader(rfile, fieldnames=["name", "gender", "pop"])
                next(reader) # Skip the header
    
                for row in reader: 
                    # Ignore names below the pop cutoff
                    if int(row["pop"]) < pop_cutoff:
                        continue
    
                    # Ignore non unique names
                    elif row["name"] in all_names:
                        continue
    
                    if row["gender"] == "F":
                        if len(young_f_names) >= young_f_num_spkrs:
                            continue
                        all_names.add(row["name"])
                        young_f_names.add(row["name"])
                    else:
                        if len(no_age_m_names) >= no_age_m_num_spkrs:
                            continue
                        all_names.add(row["name"])
                        no_age_m_names.add(row["name"])


    for year in old_range:
        with open(config.RAW_DATA_DIR / "names" / f"yob{year}.txt", "r") as rfile:
            reader = csv.DictReader(rfile, fieldnames=["name", "gender", "pop"])
            next(reader) # Skip the header

            for row in reader: 
                # Ignore names below the pop cutoff
                if int(row["pop"]) < pop_cutoff:
                    continue

                # Ignore non unique names
                elif row["name"] in all_names:
                    continue

                if row["gender"] == "M":
                    if len(old_m_names) >= old_m_num_spkrs:
                        continue
                    all_names.add(row["name"])
                    old_m_names.add(row["name"])
                else:
                    if len(no_age_f_names) >= no_age_f_num_spkrs:
                        continue
                    all_names.add(row["name"])
                    no_age_f_names.add(row["name"])
                

    return {
        "old_m_names": list(old_m_names),
        # "old_f_names": list(old_f_names),
        "middle_aged_m_names": list(middle_aged_m_names),
        "middle_aged_f_names": list(middle_aged_f_names),
        "adult_m_names": list(adult_m_names),
        "adult_f_names": list(adult_f_names),
        # "young_m_names": list(young_m_names),
        "young_f_names": list(young_f_names),
        "no_age_m_names": list(no_age_m_names),
        "no_age_f_names": list(no_age_f_names),
    }

    

if __name__ == "__main__":
    main()