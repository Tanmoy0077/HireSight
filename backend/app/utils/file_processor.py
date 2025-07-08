import PyPDF2
import io


class FileProcessor:
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Error processing PDF: {str(e)}")

    @staticmethod
    def extract_text(filename: str, file_content: bytes) -> str:
        if filename.lower().endswith(".pdf"):
            return FileProcessor.extract_text_from_pdf(file_content)
        elif filename.lower().endswith(".txt"):
            return file_content.decode("utf-8")
        else:
            raise ValueError("Unsupported file format")
