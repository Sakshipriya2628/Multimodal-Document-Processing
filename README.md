# Multimodal-Document-Processing

#### **Project Overview**
This project aims to develop an advanced student assessment grading model that evaluates student submissions by grading them and identifying areas for improvement. Unlike traditional models that only consider textual content, this model leverages GPT-4 Vision to analyze and extract insights from various forms of data, including text, images, tables, and charts.

#### **Problem Statement**
The challenge in student assessment has traditionally been the limited scope of analysis, primarily focused on text. However, student submissions often include other forms of data, such as images, tables, and charts, which are crucial for a comprehensive evaluation. Our objective was to create a grading model that can analyze these diverse data formats, providing a more accurate and holistic assessment.

#### **Solution Approach**
To address the challenge, we utilized GPT-4 Vision, which allows us to extract and interpret not only textual data but also images, tables, and charts. The solution involves the following steps:

1. **PDF to Image Conversion**: 
   - Initially, the student submissions, typically in PDF format, are converted into images to facilitate the extraction of non-textual data.
   
2. **Text Extraction**:
   - The text data is extracted separately from the image using OCR (Optical Character Recognition) techniques. This allows us to handle the textual content efficiently.

3. **Image Description Extraction**:
   - If the document contains images, GPT-4 Vision is used to generate descriptive insights about these images. This helps in understanding the context and relevance of the images in the submission.

4. **Table Data Extraction**:
   - Tables present in the document are extracted and converted into JSON format. This structured representation of data allows for easier analysis and interpretation.

5. **Chart and Graph Analysis**:
   - Charts and statistical graphs are analyzed to pull out key insights. GPT-4 Vision is utilized to interpret these visual data elements, enabling the model to understand and assess them effectively.

#### **Technologies Used**
- **GPT-4 Vision**: For interpreting and extracting insights from images, tables, and charts.
- **OCR**: For extracting text from images.
- **JSON**: For structuring table data for analysis.

#### **Code Overview**
The code for this project is structured to handle the various stages of the data extraction and analysis process. Key modules include:

- **PDF to Image Conversion Module**: Converts PDF documents into images.
- **Text Extraction Module**: Extracts text data from images using OCR.
- **Image Description Module**: Generates descriptions for images using GPT-4 Vision.
- **Table Data Extraction Module**: Extracts tables and converts them into JSON format.
- **Chart Analysis Module**: Analyzes charts and statistical graphs to pull out key insights.
