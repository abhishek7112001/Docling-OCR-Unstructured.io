import pypdf

def extract_text_from_pdf(pdf_path):
    
    reader = pypdf.PdfReader(pdf_path)
    for page in reader.pages:
        text = page.extract_text()
        if text and text.strip():
            print(text)
            return "Digital PDF"
    return "Scanned PDF"

res1 = extract_text_from_pdf("../scanned_sample.pdf")
res2 = extract_text_from_pdf("../digital_sample.pdf")

print(res1)
print(res2)