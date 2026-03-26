from unstructured.partition.pdf import partition_pdf
def detect_scanned_or_digital(file_path):
    elements = partition_pdf(filename=file_path, 
                             strategy="fast"  # skips OCR entirely)
                            )

    total_text_len =0

    for element in elements:
        # print(element)
        total_text_len+=len(str(element))
    
    if total_text_len>0:
        return "Digital PDF"
    else:
        return "Scanned PDF"

res1 = detect_scanned_or_digital("../digital_sample.pdf")
res2 = detect_scanned_or_digital("../scanned_sample.pdf")

print(res1)
print(res2)