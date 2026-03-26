def temp(file_path):

    with open(file_path, "rb") as f:
        content = f.read()
    text_content = content.decode(errors="ignore")  # converting bytes to string for searching

    if "BT" in text_content:
        # print(text_content)
        return "Digital PDF"
    else:
        return "Scanned PDF"
    
res1 = temp("../digital_sample.pdf")
res2 = temp("../scanned_sample.pdf")
print(res1)
print(res2)