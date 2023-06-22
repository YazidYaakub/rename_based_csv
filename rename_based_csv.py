import pandas as pd
from pathlib import Path
import shutil

# Load CSV data
df = pd.read_csv(r'C:\Users\myazidagmyaakub.agmy\Downloads\file_renaming - slicedoc.csv')

df = df.dropna(subset=['Filename', 'Renamed Docs'])

# Define the directory to look for
directory = Path('C:/Users/myazidagmyaakub.agmy/Downloads/Transformation')

# Create the destination directory if it doesn't exist
destination = Path('C:/Users/myazidagmyaakub.agmy/Downloads/dup/Transformation')
destination.mkdir(exist_ok=True)

# Create a new DataFrame to store the old and new filenames
dup_oldname = []
dup_newname = []
dup_filepath = []
# Go through each row in the DataFrame
for index, row in df.iterrows():
    # Find all the files with the original name in all folders
    for file in directory.glob('**/*' + row['Filename']):
        # Try to rename the file
        try:
            file.rename(file.parent / row['Renamed Docs'])
        # If a file with the new name already exists, rename with "- duplicate" added
        except FileExistsError:
            print(f'File dups: {file}')
            # shutil.copy(file, destination / file.name)
            relative_path = file.relative_to(directory)
            dest_file = destination / relative_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(file, dest_file)
            # file.rename(file.parent / (row['Renamed'].rsplit('.', 1)[0] + ' - duplicate.' + row['Renamed'].rsplit('.', 1)[1]))
            new_name = file.parent / (row['Renamed Docs'].rsplit('.', 1)[0] + ' - duplicate.' + row['Renamed Docs'].rsplit('.', 1)[1])
            file.rename(new_name)
            # renamed_files.append({'Old Name': file.name, 'New Name': new_name.name})
            dup_filepath.append(file)
            dup_oldname.append(file.name)
            dup_newname.append(new_name.name)

        except FileNotFoundError:
            print(f'File not found: {file}')

dup_df = pd.DataFrame({"Old Name": dup_oldname,
                      "Renamed" : dup_newname,
                      "File Path": dup_filepath})

            
dup_df.to_csv('dups_trasnformation.csv', index=False)
print("Done")
