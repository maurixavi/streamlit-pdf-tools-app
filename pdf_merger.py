import streamlit as st
import PyPDF2

def merge_pdfs(output_path, pdf_documents):
  pdf_merger = PyPDF2.PdfMerger()
  
  for pdf_document in pdf_documents:
    pdf_merger.append(pdf_document)
  
  with open(output_path, 'wb') as output_file:
    pdf_merger.write(output_file)


def app():
  st.header('Merge PDF Files')
  st.write('Combine multiple PDF files into a single new document.')
  st.image('assets/pdf_image.jpg', width=150)
  
  uploaded_files = st.file_uploader(label='Upload PDF files', accept_multiple_files=True, type=['pdf'])
  
  if uploaded_files:
  
    merge_btn = st.button(label='Merge PDF')
    if merge_btn:
      
      if len(uploaded_files) <= 1:
        st.warning('Please select multiple PDF files')
        
      else:
        output_pdf = 'assets/pdf_merged.pdf'
        merge_pdfs(output_pdf, uploaded_files)
        st.success('PDF files correctly combined')

        # Resulting PDF content
        with open(output_pdf, 'rb') as file:
          pdf_data = file.read()
            
        # Download generated PDF
        st.download_button(label='Download', data=pdf_data, file_name='merged.pdf')
     

#if __name__ == '__main__':
#  main()