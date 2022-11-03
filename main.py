import pandas
import json
import hashlib

# Receive file path as input from user
file_path = input("Please enter the csv file path: ").strip()

def Generate_Hash_CSV(file_path):
    # CREATE A PANDAS DTAFRAME WITH DATA FROM THE CSV FILE
    nft_df = pandas.read_csv(file_path)
    # CREATE A DICTIONARY TO STORE JSON EQUIVALENT OF EACH ROW IN THE DATAFRAME 
    data_dict = {}
    # LOOP THROUGH EACH ROW IN THE DATA FRAME TO CREATE A DICTIONARY THAT CONFORMS TO THE NFT CHIP-0007 FORMAT
    for (index, row) in nft_df.iterrows():
            new_data =  { row.filename: {
            "format": "CHIP-0007",
            "name": row.filename,
            "description": row.description,
            "minting_tool": "SuperMinter/2.5.2",
            "sensitive_content": False,
            "series_number": row.serialnumber,
            "series_total": 1000,
            "collection": {
                "name": f"Example {row.filename} collection",
                "id": row.uuid,
                "attributes": [
                    {
                        "type": "description",
                        "value": f"Example {row.filename} collection is the best {row.filename} collection. Get yours today!"
                    },
                    {
                        "type": "icon",
                        "value": f"https://{row.filename}.com/image/icon.png"
                    },
                    {
                        "type": "banner",
                        "value": f"https://{row.filename}.com/image/banner.png"
                    },
                    {
                        "type": "twitter",
                        "value": f"Example{row.filename}"
                    },
                    {
                        "type": "website",
                        "value": f"https://example{row.filename}collection.com/"
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
        new_dataframe = pandas.read_csv(file_path)
        # Loop through the new dataframe and replace all the rows under the hash column with the hash value of the json
        for (index, row) in new_dataframe.iterrows():
            new_dataframe.loc[index, "hash"] = hash_value
        # Create a new csv file with the updated changes
        new_dataframe.to_csv(f"{file_path.rstrip('.csv')}.output.csv")

# Call Function to generate new CSV with Hash
Generate_Hash_CSV(file_path)