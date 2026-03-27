"""
Парсер резюме из PDF, DOCX, TXT
"""

import os

# Попробуем импортировать библиотеки, если они не установлены, выдадим ошибку
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    from docx import Document
except ImportError:
    Document = None


class ResumeParser:
    """Извлекает текст из файла резюме"""

    @staticmethod
    def extract_text(file_path: str) -> str:
        """Извлекает текст из файла в зависимости от расширения"""
        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.pdf':
            return ResumeParser._extract_pdf(file_path)
        elif ext == '.docx':
            return ResumeParser._extract_docx(file_path)
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Неподдерживаемый формат: {ext}")

    @staticmethod
    def _extract_pdf(file_path: str) -> str:
        """Извлечение текста из PDF, сначала пробуем pdfplumber (точнее), затем PyPDF2"""
        text = ""
        if pdfplumber:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        elif PyPDF2:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
        else:
            raise ImportError("Не установлена ни одна библиотека для PDF. Установите pdfplumber или PyPDF2.")
        return text

    @staticmethod
    def _extract_docx(file_path: str) -> str:
        """Извлечение текста из DOCX"""
        if not Document:
            raise ImportError("python-docx не установлен.")
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])