import pandas as pd
import os
import re
import json
import time
import openai
# import tiktoken
#import PyPDF2
from docx import Document
from dotenv import load_dotenv, find_dotenv
from typing import List, Dict
from datetime import datetime
import langchain
from openai import AzureOpenAI
import logging


load_dotenv()

api_key = os.environ.get('AZURE_VISION_API_KEY')
api_url = os.environ.get('vision_base_url')

client = AzureOpenAI(
  azure_endpoint = api_url, 
  api_key=api_key,  
  api_version="2023-12-01-preview"
)
model="gpt4-vision-preview"



def get_file_paths(folder_path):
    import os

    file_paths = []
    # List all files and sort them to ensure they are processed sequentially
    for filename in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, filename)
        # check if the path is a file (not a directory)
        if os.path.isfile(file_path):
            file_paths.append(file_path)

    return file_paths

def image_selection(file_path):
    import base64
    with open(file_path, 'rb') as image_file:
        binary_content = image_file.read()

    # Encode the bytes to a Base64 string
    base64_encoded_str = base64.b64encode(binary_content)
    # Convert bytes to a string (Python 3)
    base64_encoded_str = base64_encoded_str.decode('utf-8')
    data_url = f'data:image/png;base64,{base64_encoded_str}'
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": """You are an image analyser and tasked with describing the input image according to the following instructions:
         1. Go through each of the images one by one and then give the description of each image one by one along with the image name of each.
         2. The images may contain texts, tables, charts, graphical data, statistical data and many other information submitted by students in their 
         project depending on image to image.
        You have to understand the information in each page very carefully and do the following tasks for each image:
         1. Extract texts if text is present.
         2. If a table is present extract the table data in correct JSON format strictly.
         3.If there are graphs, visual charts or other informational elements, go through them, "Read them", "Understand Them",
         and then "Give Description" for each element of them. MAKE SURE TO KEEP DESCRIPTION DESCRIPTIVE.
         4. Also give each element a reference for example if there are two tables in a file give each table a reference, similarly do the same for visuals also.

        Be careful, it's a submission even the minute details and information matters a lot for grading. You need to be accurate and very careful 
         while answering."""},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": data_url,
                    },
                },
            ],
        }
    ]
    return messages

def describe_images(folder_path):
    """Print the description for each image in the given folder."""
    file_paths = get_file_paths(folder_path)
    for file_path in file_paths:
        try:
            print(f"########## Starting analysis for Image {file_paths.index(file_path) + 1} ##########\n")
            messages = image_selection(file_path)
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=4000,
            )
            print(f"The description for Image {file_paths.index(file_path) + 1} is \n{resp.choices[0].message.content}\n")
            print("########## End of analysis ##########\n")
        except Exception as e:
            logging.error(f"Failed to process file {file_path}: {e}")

if __name__ == "__main__":
    folder_path = '/Users/sakshi_admin/Downloads/Baltic'
    describe_images(folder_path)
