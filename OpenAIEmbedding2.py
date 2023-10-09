

import openai
import pandas as pd
import time
import csv
import os

# Initialize OpenAI API with your key
openai.api_key = "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"

# Define the file path
file_path = 'C:/Users/karam/PycharmProjects/skillExtraction/skillstitles_de.xlsx'

# Read the Excel file into a pandas DataFrame
input_df = pd.read_excel(file_path)

# Define the output file path
output_file_path = 'output.txt'

# Create a set to store existing words from the output file
existing_words = set()

# Check if the output file exists
if os.path.exists(output_file_path):
    # Read the existing output file and add the words to the set
    with open(output_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            existing_words.add(row[0])


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    try:
        # Call the OpenAI API to get the embedding
        embedding = openai.Embedding.create(input=text, model=model)['data'][0]['embedding']
        return embedding
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


# Open the output file for writing
with open(output_file_path, 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='\t')

    # Initialize a counter for requests
    request_counter = 0

    # Iterate over rows of the input DataFrame
    for index, row in input_df.iterrows():
        text = row[0]  # assuming the text is in the first column of the DataFrame

        # Check if the word is already in the output file
        if text in existing_words:
            print(f"Word '{text}' was already there.")
            continue

        embedding = get_embedding(text)

        if embedding is not None:
            # Write the key-value pair to the output file
            writer.writerow([text, embedding])
            print(f"Line {index} was written.")

            # Increment the request counter
            request_counter += 1

            # Sleep for 20 seconds every 3 requests
            if request_counter % 3 == 0:
                time.sleep(60)
        else:
            # Break the loop if an error occurred
            print("Breaking the loop due to an error.")
            break
