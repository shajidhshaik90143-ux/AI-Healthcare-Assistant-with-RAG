from pathlib import Path
import fitz


def load_pdf(pdf_path):

    pdf_path = Path(pdf_path)

    documents = []

    pdf = fitz.open(pdf_path)

    for page_number, page in enumerate(pdf, start=1):

        text = page.get_text("text")

        if text and text.strip():

            documents.append({
                "text": text.strip(),
                "page": page_number,
                "file": pdf_path.name
            })

    pdf.close()

    return documents


def load_all_pdfs(directory="data/medical_documents"):

    directory = Path(directory)

    directory.mkdir(
        parents=True,
        exist_ok=True
    )

    all_documents = []

    for pdf_file in directory.glob("*.pdf"):

        try:
            documents = load_pdf(pdf_file)
            all_documents.extend(documents)

        except Exception as error:

            print(
                f"Error loading {pdf_file}: {error}"
            )

    return all_documents