import os
import pandas as pd
import requests

# Create 'preview' directory if it doesn't exist
if not os.path.exists('preview'):
    os.makedirs('preview')

# Read the CSV file
df = pd.read_csv('result.csv')

# Download each image
for index, row in df.iterrows():
    url = row['image']
    filename = os.path.join('preview', url.split("/")[-1])
    response = requests.get(url, stream=True)

    # Check if the image was retrieved successfully
    if response.status_code == 200:
        # Save the image received into the file
        with open(filename, 'wb') as out_file:
            out_file.write(response.content)
        print(f'Image {index}th saved to {filename}')
    else:
        print(f'Error - could not download {url}')

print('Image download completed.')
