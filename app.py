import streamlit as st
import os
from PyPDF2 import PdfFileReader
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

def convert_pdf_to_images(pdf_file_path, first_page, last_page):
    return convert_from_path(pdf_file_path, first_page=first_page, last_page=last_page)

def convert_image_to_text(image):
    return pytesseract.image_to_string(image, lang='vie', config=custom_config)

def process_pdf(pdf_file):
    images = convert_pdf_to_images(pdf_file.name, first_page=1, last_page=1)

    text = ''
    for idx, image in enumerate(images):
        text += convert_image_to_text(image) + '\n'

    return text

# Set Tesseract path
custom_config = r'--oem 3 --psm 3'
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Streamlit app
st.title("PDF to Text Conversion")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Display uploaded file
    st.image("https://img.icons8.com/plasticine/2x/pdf.png", use_column_width=True)
    st.write(f"File Name: {uploaded_file.name}")

    # Process PDF and display text
    text_output = process_pdf(uploaded_file)
    st.subheader("Extracted Text:")
    st.text(text_output)

    # Save text to a file
    save_button = st.button("Save Text to File")
    if save_button:
        with open('output.txt', 'w') as file:
            file.write(text_output)
        st.success("Text saved to 'output.txt'")

        # Download link for the saved file
        st.markdown(
            f"### [Download Saved Text](sandbox:/path/to/your/output.txt)"
        )
