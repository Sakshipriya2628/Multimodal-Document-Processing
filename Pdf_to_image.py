from pdf2image import convert_from_path
import os

def convert_pdf_to_images(pdf_path, output_folder, dpi=300):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert PDF to images
    images = convert_from_path(pdf_path, dpi=dpi)

    # Save images to output folder
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'page_{i+1}.png')
        image.save(image_path, 'PNG')
        print(f'Saved {image_path}')

# Usage example
pdf_file_path = '/Users/sakshi_admin/Desktop/Image Assessment POC/Baltic Submissions/Pdf Submissions/Baltic5.pdf'  # Change this to the path of your PDF
output_directory = 'Baltic 5 output_images'  # Change this to your desired output folder
convert_pdf_to_images(pdf_file_path, output_directory)
