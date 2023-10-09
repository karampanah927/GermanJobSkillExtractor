import os
from bs4 import BeautifulSoup

def remove_html_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Using BeautifulSoup to parse the content and extract text without tags
    soup = BeautifulSoup(content, 'lxml')
    cleaned_text = soup.get_text()

    # Write the cleaned text back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            remove_html_from_txt(file_path)
            print(f"Processed {filename}")

# Usage
folder = "C:\\Users\\karam\\PycharmProjects\\GermanJobSkillExtractor\\jobpostings"
process_folder(folder)
