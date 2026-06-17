import fitz
from pathlib import Path

def text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    if doc is None:
        return "PDF file not found"
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    if text == "":
        return "PDF contains no text"
    return text

def clean_text(text):
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.lower().startswith("page") or line.isdigit():
            continue
        line = ''.join(line.split())
        cleaned_lines.append(line)
    return  "\n".join(cleaned_lines)

def chunk_text(text, pdf_path, page_no, chunk_size, overlap):
    words = text.split()
    chunks = []
    chunk_id = 1
    step = chunk_size - overlap
    for i in range(0, len(words), step):
        chunk_words = words[i:chunk_size+i]
        chunk_text = ' '.join(chunk_words)
        chunk_data = {
            "text" : chunk_text,
            "data" : {
                "chunk_id": chunk_id,
                "source_file": pdf_path,
                "page": page_no
            }
        }
        chunks.append(chunk_data)
        chunk_id += 1
        if i + chunk_size >= len(words):
            break
    return chunks
if __name__ == "__main__":
    pdf_path = "test.pdf"
    text = text_from_pdf(pdf_path)
    clean_text(text)
    page_no = 3
    print(chunk_text(text, pdf_path, page_no, chunk_size=400, overlap=60))
