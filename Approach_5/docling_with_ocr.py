from docling.document_converter import DocumentConverter

def detect_pdf_type(file_path):
    converter = DocumentConverter()
    result =converter.convert(file_path)
    extracted_text= result.document.export_to_text()

    if(len(extracted_text)>0):
        json_output = result.document.export_to_dict()
        return {
            "type": "Digital PDF",
            "data": json_output
        }
    else:
        return {
            "type": "Scanned PDF",
            "message": "No readable text found"
        }
    
res1 = detect_pdf_type("../digital_sample.pdf")
res2 = detect_pdf_type("../scanned_sample.pdf")

print(res1)
print("*******************************************************")
print("*******************************************************")
print("*******************************************************")
print("*******************************************************")
print("*******************************************************")
print("*******************************************************")
print("*******************************************************")
print("*******************************************************")
print(res2)