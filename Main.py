import pandas as pd
import os
import re
import json
import time
import logging
import base64
from docx import Document
from dotenv import load_dotenv, find_dotenv
from typing import List, Dict
from datetime import datetime
from openai import AzureOpenAI

load_dotenv()

api_key = os.environ.get('AZURE_VISION_API_KEY')
api_url = os.environ.get('vision_base_url')

client = AzureOpenAI(
    azure_endpoint=api_url, 
    api_key=api_key,  
    api_version="2023-12-01-preview"
)
model="gpt4-vision-preview"

# Ensure logging is set up to capture any errors
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_file_paths(folder_path):
    file_paths = []
    for filename in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_paths.append(file_path)
    return file_paths

def image_selection(file_path):
    with open(file_path, 'rb') as image_file:
        binary_content = image_file.read()
    base64_encoded_str = base64.b64encode(binary_content).decode('utf-8')
    data_url = f'data:image/png;base64,{base64_encoded_str}'
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": """You are an image analyser and tasked with describing the input image according to the following instructions:
         1. Go through image minutely and word by word.
         2. Do not break the image sequence in the directory.
         3. The images will contain texts, tables, charts, graphical data, statistical data and many other information submitted by students in their 
            project depending on image to image.
         4. Take a deep breathe and let's go step by step, in case of graphical data (pie charts and line charts) analyse minutely and generate the first draft and iterate on the results generated.
         5. Before giving the final output make sure to recheck the response generated with the actual file.
         6. You have to label each element in the image for example if in a image it has two different tables then name them Table A and
            Table B respectively. 
         7. Similary if you have multiple charts in a image then name them as Chart A, chart B and so on.....
         8. Make sure to give the "JSON STRUCTURE" for "ALL" the "Tables" IN THE IMAGE.
                 
            You have to understand the information in each page very carefully and do the following tasks for each image:
                 
         1. For texts present in image your job is to "Only Extract" text as it is in the image from start to end. We don't need summary of the textual part. 
         2. If tables are present extract the tables data in correct "JSON" format strictly with proper naming such as Table A followed by it's "JSON
            STRUCTURE" then it's description , then  Table B it's "JSON STRUCTURE" and then it's description and so on..Make sure you do it for all the
            tables , it doesn't matter if they represent same data.It should have all the table's JSON structure.
         3.If there are graphs, visual charts or other informational elements, go through them, "Read what it represents along with correct data interpretation", "Understand Them",
           and then "Give Description" for each element of the graphs and charts.. MAKE SURE TO KEEP Analysis DESCRIPTIVE along with also following
           the naming convention for example if you have multiple charts in a image then name them as Chart A then it's description, 
           chart B then it's description and so on.....
         4. In case of you don't understand what the graph , chart , pie chart, line chart is then 'Do NOT Hallucinate' , inspite display the message "Not able to Understand the VISUAL".
            and Give the picture chart or visual for which you don't understand what to interpret. But make sure you don't "Guess" anything.
                 I want the analysis to be accurate at the last.

        Be careful,it's a submission even the minute details and information matters a lot for grading. You need to be accurate and very careful 
         while answering. """},
                {"type": "image_url", "image_url": {"url": data_url}}
            ]
        }
    ]
    return messages

def describe_images(folder_path):
    file_paths = get_file_paths(folder_path)
    data = []

    for file_path in file_paths:
        try:
            logging.info(f"Starting analysis for Image {file_paths.index(file_path) + 1}")
            messages = image_selection(file_path)
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=4000,
                seed= 42,
            )
            description = resp.choices[0].message.content
            data.append({
                'Image Number': file_paths.index(file_path) + 1,
                'Image Path': file_path,
                'Description': description
            })
            logging.info("End of analysis")
        except Exception as e:
            logging.error(f"Failed to process file {file_path}: {str(e)}")

    if data:
        with open('Baltic1 Analysis1.txt', 'w') as txt_file:
            for entry in data:
                txt_file.write(f"Image Number: {entry['Image Number']}\n")
                txt_file.write(f"Image Path: {entry['Image Path']}\n")
                txt_file.write(f"Description: {entry['Description']}\n")
                txt_file.write("--------------------------------------------------\n")
            logging.info("Data successfully written to text file.")
    else:
        logging.warning("No data collected. Check the input folder and image processing.")

if __name__ == "__main__":
    folder_path = '/Users/sakshi_admin/Desktop/Image Assessment POC/Baltic 1 output_images'
    describe_images(folder_path)
