import streamlit as st
from streamlit import session_state as ss
from streamlit_pdf_viewer import pdf_viewer
import PyPDF2

def get_pages_to_extract(input_str, num_pages):
    pages = []
    parts = input_str.replace(' ', '').split(',') 
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            pages.extend(range(start, end + 1))
        if part.isdigit():
            page = int(part)
            pages.append(page)
    return pages


def generate_new_pdf(pdf_reader, num_pages, pages_to_extract):
    all_pages = list(range(1, num_pages + 1))
    pages_to_keep = [page for page in all_pages if page not in pages_to_extract]
        
    writer = PyPDF2.PdfWriter()
    for page_num in pages_to_keep:
        adjusted_page_num = page_num - 1
        writer.add_page(pdf_reader.pages[adjusted_page_num])

    output_pdf_path = "output.pdf"
    with open(output_pdf_path, "wb") as fp:
        writer.write(fp)

    return output_pdf_path


def app():
    st.header('Extract PDF Pages')
    st.write('Extract pages from PDF file. Get a new document containing only the pages you want.')
    st.image('assets/pdf_image.jpg', width=150)
    
    if 'pdf_ref' not in ss:
        ss.pdf_ref = None

    # Access the uploaded ref via a key
    uploaded_pdf = st.file_uploader("Upload PDF file", type=('pdf'), key='pdf')

    if uploaded_pdf:
        # Store the PDF in session_state
        ss.pdf_ref = uploaded_pdf
        
        # Get the number of pages in the PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_pdf)
        num_pages = len(pdf_reader.pages)
        st.write(f"Number of pages in PDF: {num_pages}")

        # User input: list of page numbers to extract
        input_pages_text  = st.text_input('Input pages number to extract separated by comma or range. Example: 1, 3, 5-9')
        
        input_pages_to_extract = get_pages_to_extract(input_pages_text, num_pages)
        st.write('Extract pages: ', str(input_pages_to_extract))

        output_pdf_path = generate_new_pdf(pdf_reader, num_pages, input_pages_to_extract)

        # Resulting PDF content
        with open(output_pdf_path, "rb") as file:
            pdf_data = file.read()

        # Preview generated PDF
        preview_btn = st.button("Preview")
        if preview_btn:
            pdf_viewer(input=pdf_data, width=700)
        
        # Download generated PDF
        st.download_button(label='Download', data=pdf_data, file_name='extracted.pdf')


app()
