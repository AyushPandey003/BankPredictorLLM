from pypdf import PdfReader, PdfWriter
import io


def unlock_pdf(input_pdf_path, password, output_pdf_path=None):
    """
    Unlock a password-protected PDF file.
    
    Args:
        input_pdf_path (str): Path to the password-protected PDF
        password (str): Password to unlock the PDF
        output_pdf_path (str, optional): Path to save the unlocked PDF. 
                                       If None, saves as 'unlocked_' + original filename
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        reader = PdfReader(input_pdf_path)
        reader.decrypt(password)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        if output_pdf_path is None:
            import os
            base_name = os.path.basename(input_pdf_path)
            output_pdf_path = f"unlocked_{base_name}"

        with open(output_pdf_path, "wb") as f:
            writer.write(f)

        print(f"PDF unlocked successfully! Saved as: {output_pdf_path}")
        return True
        
    except Exception as e:
        print(f"Error unlocking PDF: {str(e)}")
        return False


def unlock_pdf_from_bytes(pdf_bytes, password):
    """
    Unlock a password-protected PDF from bytes in memory.
    
    Args:
        pdf_bytes (bytes): PDF file content as bytes
        password (str): Password to unlock the PDF
    
    Returns:
        bytes: Unlocked PDF as bytes, or None if failed
    """
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        reader.decrypt(password)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        output_buffer = io.BytesIO()
        writer.write(output_buffer)
        output_buffer.seek(0)
        return output_buffer.getvalue()
        
    except Exception as e:
        print(f"Error unlocking PDF from bytes: {str(e)}")
        return None


def is_pdf_password_protected(pdf_path_or_bytes):
    """
    Check if a PDF is password protected.
    
    Args:
        pdf_path_or_bytes: Either file path (str) or PDF bytes
    
    Returns:
        bool: True if password protected, False otherwise
    """
    try:
        if isinstance(pdf_path_or_bytes, str):
            reader = PdfReader(pdf_path_or_bytes)
        else:
            reader = PdfReader(io.BytesIO(pdf_path_or_bytes))
        
        # Try to access pages - will raise exception if password protected
        _ = len(reader.pages)
        return False
    except Exception:
        return True


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     # Test with file path
#     success = unlock_pdf("path/to/protected.pdf", "your_password")
#     
#     # Test password protection check
#     is_protected = is_pdf_password_protected("path/to/your.pdf")
#     print(f"PDF is password protected: {is_protected}")
