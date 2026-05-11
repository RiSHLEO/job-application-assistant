import re
from pypdf import PdfReader
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file given as bytes."""
    try:
        pdf_reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return clean_text(text)
    except Exception as e:
        raise ValueError(f"Could not extract text from PDF: {str(e)}")

def clean_text(text: str) -> str:
    """Clean extracted text by removing excessive whitespace."""
    # Remove excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove excessive spaces
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def truncate_text(text: str, max_chars: int = 3000) -> str:
    """Truncate text to avoid exceeding token limits."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n[CV truncated due to length...]"