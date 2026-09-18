from pathlib import Path


def ensure_directories():

    directories = [
        "data",
        "data/medical_documents",
        "data/processed",
        "assets"
    ]

    for directory in directories:
        Path(directory).mkdir(
            parents=True,
            exist_ok=True
        )


def format_source(metadata):

    file_name = metadata.get(
        "file",
        "Unknown document"
    )

    page = metadata.get(
        "page",
        "Unknown"
    )

    return f"{file_name} — Page {page}"