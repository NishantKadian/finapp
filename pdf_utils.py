def read_pdf_as_bytes(file_path: str) -> bytes:
    """
    Read a PDF file and return its contents as bytes.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        bytes: Contents of the PDF file
    """
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"PDF file not found at {file_path}")
    except Exception as e:
        raise Exception(f"Error reading PDF file: {str(e)}")
