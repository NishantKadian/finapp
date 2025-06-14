from pdf_utils import read_pdf_as_bytes

# Example usage
pdf_path = "path/to/your/pdf/file.pdf"
pdf_bytes = read_pdf_as_bytes(pdf_path)
print(f"PDF size: {len(pdf_bytes)} bytes")
