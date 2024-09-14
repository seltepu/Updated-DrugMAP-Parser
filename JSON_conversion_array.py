import json

# reading the input file and all of its lines
with open('08_Drug_to_DME_Mapping_Information_Multiple.txt', 'r') as file:
    data = file.readlines()


# Skipping first 9 header lines
start_line = 0
for index, line in enumerate(data):
    if line.strip().startswith("EI: "): # checking for line which starts with relevant info
        start_line = index + 1 # going down lines, adding 1 to eventually reach line to start from
        break


# setting right side of colon values to none for later
dme_id = dme_name = drug_id = drug_name = reference_name = reference_url = None

# creating an empty list to hold all the JSON objects
array_json_objects = []

# getting all json objects starting from after the header ending
for line in data[start_line:]:
    parts = line.strip().split("\t")
    
    # takes all parts of input file below sets of colons for data
    if len(parts) < 3:
        continue
    
    # ex. in ['DE4LYSA', 'DI', 'DMIKQH5'] <-- key is DI and Value is DMIKQH5
    key = parts[1]
    value = parts[2]
    
    
    # assigning variable names based on categorical info specified in colons section
    if key == "EI":
        dme_id = value
    elif key == "EN":
        dme_name = value
    elif key == "DI":
        drug_id = value
    elif key == "DN":
        drug_name = value
    elif key == "RN":
        reference_name = value
    elif key == "RU":
        reference_url = value


    # checking all values have been assigned "non-none" values before proceeding and creating json object <-- makes sure invalid entries aren't included
    if dme_id and dme_name and drug_id and drug_name and reference_name and reference_url:

        # splitting reference url into 2 parts(before and after "term") and taking last value for id
        pmid = reference_url.split("term=")[-1]

        # creating the JSON object
        json_obj = {
            "_id": f"{dme_id}-METABOLIZES-{drug_id}",
            "_version": 1,
            "object": {
                "name": drug_name,
                "id": drug_id
            },
            "predicate": "metabolizes",
            "predication": [
                {
                    "pmid": pmid
                }
            ],
            "subject": {
                "name": dme_name,
                "id": dme_id
            }
        }
                
        # adding newly formatted json object to the array
        array_json_objects.append(json_obj)  
    
        # Resetting all variables to None to get values for upcoming JSON objects and adding them to array
        dme_id = dme_name = drug_id = drug_name = reference_name = reference_url = None

# outputting the JSON object into a file
with open('formatted_json_array.json', 'w') as f:
    json.dump(array_json_objects, f, indent=2)
