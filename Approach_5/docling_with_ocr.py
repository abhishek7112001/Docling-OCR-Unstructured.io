import re
import html
import unicodedata
from docling.document_converter import DocumentConverter


def clean_docling_markdown(md: str) -> str:
    md = html.unescape(md)
    md = unicodedata.normalize("NFKC", md)
    md = re.sub(r"[\u200b-\u200d\uFEFF]", "", md)

    replacements = {
        "\u2013": "-", "\u2014": "-", "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u00a0": " ",
        "\u00a0": "", "ﬁ": "fi", "ﬂ": "fl", "\u00ad": "", "\u00a0": " ",
    }
    for old, new in replacements.items():
        md = md.replace(old, new)

    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"[ \t]+", " ", md)
    md = re.sub(r"(?m)^[ ]+$", "", md)

    return md.strip()


def detect_pdf_type(file_path, output_path):
    converter = DocumentConverter()
    result = converter.convert(file_path)
    extracted_text = result.document.export_to_text()

    if len(extracted_text.strip()) > 0:
        markdown_output = result.document.export_to_markdown()
        cleaned_markdown = clean_docling_markdown(markdown_output)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cleaned_markdown)

        return {
            "type": "Markdown",
            "saved_to": output_path
        }
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("No readable text found")

        return {
            "type": "Markdown",
            "saved_to": output_path,
            "warning": "No readable text found"
        }


res1 = detect_pdf_type("../digital_sample.pdf", "digital_output.md")
res2 = detect_pdf_type("../scanned_sample.pdf", "scanned_output.md")

print(res1)
print(res2)