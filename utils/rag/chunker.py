import re
from typing import List


# --------------------------------------------------
# Clean Resume Text
# --------------------------------------------------

def clean_text(text: str) -> str:
    """
    Clean resume text before chunking.
    """

    text = text.replace("\t", " ")

    # Remove multiple spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# --------------------------------------------------
# Split Resume into Sections
# --------------------------------------------------

def split_into_sections(text: str) -> List[str]:
    """
    Splits the resume using blank lines.

    Every section becomes a candidate chunk.
    """

    sections = re.split(r"\n\s*\n", text)

    sections = [

        section.strip()

        for section in sections

        if section.strip()

    ]

    return sections


# --------------------------------------------------
# Merge Small Sections
# --------------------------------------------------

def merge_small_chunks(
    sections: List[str],
    min_chunk_size: int = 120
) -> List[str]:
    """
    Merge very small sections with the previous one.

    Prevents tiny chunks like:

    Skills

    Python

    Java
    """

    chunks = []

    buffer = ""

    for section in sections:

        if len(buffer) < min_chunk_size:

            buffer += "\n\n" + section

        else:

            chunks.append(buffer.strip())

            buffer = section

    if buffer:

        chunks.append(buffer.strip())

    return chunks


# --------------------------------------------------
# Main Chunking Function
# --------------------------------------------------

def create_chunks(resume_text: str) -> List[str]:
    """
    Creates semantic chunks from resume text.
    """

    resume_text = clean_text(resume_text)

    sections = split_into_sections(
        resume_text
    )

    chunks = merge_small_chunks(
        sections
    )

    return chunks
