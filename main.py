import pandas
import json
import hashlib
from csv import DictReader, DictWriter


# Receive file path as input from user
csv_file_path = input("Please enter the csv file path: ").strip()
# csv_file_path = "HNGi9_CSV_FILE_2.csv"


def Format_CSV(csv_file_path):
    # OPEN THE CSV FILE AND CONVERT TO A DATAFRAME USING PANDAS
    new_df = pandas.read_csv(csv_file_path)
    # CREATE A LIST OF ALL THE COLUMN NAMES IN THE DATAFRAME
    df_columns_list = new_df.columns
    # LOOP THROUGH THE COLUMNS NAMES IN THE LIST AND FORMAT THE NAMES IN THE DATAFRAME TO BE LOWERCASE WITHOUT WHITESPACE
    for column in df_columns_list:
        new_df.rename(columns={column: column.lower().strip().replace(" ","")}, inplace=True)
    # SAVE THE CHANGES TO THE CSV FILE
    new_df.to_csv(csv_file_path, index=False)


def Generate_Hash_CSV(csv_file_path):
    # CAll THE FUNCTION TO FORMAT THE CSV BEFORE GENERATING THE HASH
    Format_CSV(csv_file_path)
    # CREATE A PANDAS DATAFRAME WITH DATA FROM THE CSV FILE
    nft_df = pandas.read_csv(csv_file_path)
    # CREATE A DICTIONARY TO STORE JSON EQUIVALENT OF EACH ROW IN THE DATAFRAME 
    data_dict = {}
    # LOOP THROUGH EACH ROW IN THE DATA FRAME TO CREATE A DICTIONARY THAT CONFORMS TO THE NFT CHIP-0007 FORMAT
    for (index, row) in nft_df.iterrows():
            new_data =  { row.filename: {
            "format": "CHIP-0007",
            "name": row.name ,
            "description": row.description,
            "minting_tool": str(row.teamnames),
            "sensitive_content": False,
            "series_number": row.seriesnumber,
            "series_total": row.seriesnumber,
            "collection": {
                "name": f"Example {row.name} collection",
                "id": row.uuid,
                "attributes": [
                    {
                        "type": "description",
                        "value": f"Example {row.name} collection is the best {row.name} collection. Get yours today!"
                    },
                    {
                        "type": "icon",
                        "value": f"https://{row.name}.com/image/icon.png"
                    },
                    {
                        "type": "banner",
                        "value": f"https://{row.name}.com/image/banner.png"
                    },
                    {
                        "type": "twitter",
                        "value": f"Example{row.name}"
                    },
                    {
                        "type": "website",
                        "value": f"https://example{row.name}collection.com/"
                    }
                ]
            }
            }
            }
            # UPDATE DICTIONARY WITH EACH JSON FILE DATA AFTER CONVERISON
            data_dict.update(new_data)
    
    #CREATE A JSON FILE CONTAINING ALL THE DATA FROM THE CSV IN THE CHIP-0007 FORMAT
    with open("hash_data.json", "w") as new_file:
            json.dump(data_dict, new_file, indent=4)                

    # CALCULATE THE 256 HASH OF THE JSON FILE
    sha256_hash = hashlib.sha256()
    with open("hash_data.json", "rb") as new_file:
        for byte_block in iter(lambda: new_file.read(4096), b""):
            sha256_hash.update(byte_block)
        # Save hash value in a variable
        hash_value = sha256_hash.hexdigest()
        print(hash_value)

        # Create a new dataframe
        new_dataframe = pandas.read_csv(csv_file_path)
        # Loop through the new dataframe and replace all the rows under the hash column with the hash value of the json
        for (index, row) in new_dataframe.iterrows():
            new_dataframe.loc[index, "hash"] = hash_value
        # Create a new csv file with the updated changes
        new_dataframe.to_csv(f"{csv_file_path.rstrip('.csv')}.output.csv", index=False)


# Call Function to generate new CSV with Hash
Generate_Hash_CSV(csv_file_path)