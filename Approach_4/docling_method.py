from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import PdfFormatOption

def detect_pdf_type(file_path):
    # Disable OCR so scanned PDFs return no text
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False  # <-- Key fix (disable OCR)

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    result = converter.convert(file_path)
    extracted_text = result.document.export_to_text().strip()

    if len(extracted_text) > 0:
        return {
            "type": "Digital PDF",
            "data": result.document.export_to_dict()
        }
    else:
        return {
            "type": "Scanned PDF",
            "message": "No readable text found"
        }

res1 = detect_pdf_type("../digital_sample.pdf")
res2 = detect_pdf_type("../scanned_sample.pdf")

print(res1['type'])  # Digital PDF
print(res2['type'])  # Scanned PDF