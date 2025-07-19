# here im going to build my utility functions such as reading pdfs, txt files, and saving uploads
import os 
import fitz

def save_file(file):
    '''
    this function save the uploaded file to the data folder
    Args:
        file: the uploaded file
    Returns:
        file_path: the path of the saved file
    '''

    file_path = os.path.join("data" , "uploaded_files" , file.filename)
    os.makedirs(os.path.dirname(file_path),exist_ok=True)
    with open(file_path , "wb") as f:
        f.write(file.getbuffer())

    return file_path

def read_text_file(file_path):
    '''
    here we read the text file and return the text
    Args:
        file_path: the path of the file to read
    Returns:
        text: the text of the file  
    '''
    with open(file_path , 'r') as file:
        return file.read()

def read_pdf_file(file_path):
    '''
    here we read the pdf file and return the text
    Args:
        file_path: the path of the file to read
    Returns:
        text: the text of the file  
    '''
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text
def read_file(file_path):
    '''
    Read the file and return the text
    '''
    # Get the file extension in lowercase
    file_extension = os.path.splitext(file_path)[1].lower()
    
    print(f"Debug: Trying to read file {file_path} with extension {file_extension}")  # Debug line
    
    if file_extension == '.txt':
        return read_text_file(file_path)
    elif file_extension == '.pdf':
        return read_pdf_file(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")