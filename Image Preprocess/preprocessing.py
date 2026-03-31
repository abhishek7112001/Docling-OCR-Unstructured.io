import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import fitz  # PyMuPDF
import os


# ─────────────────────────────────────────
# STEP 1: Convert PDF pages to images
# ─────────────────────────────────────────
def pdf_to_images(pdf_path, dpi=300):
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
        img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
            pix.height, pix.width, 3
        )
        images.append(img_array)
    doc.close()
    return images


# ─────────────────────────────────────────
# STEP 2: Deskew (fix tilted/rotated pages)
# ─────────────────────────────────────────
def deskew(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    # Correct angle
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    deskewed = cv2.warpAffine(
        image, M, (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )
    print(f"  Deskew angle corrected: {angle:.2f}°")
    return deskewed


# ─────────────────────────────────────────
# STEP 3: Grayscale conversion
# ─────────────────────────────────────────
def to_grayscale(image: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


# ─────────────────────────────────────────
# STEP 4: Image enhancement
# ─────────────────────────────────────────
def enhance_image(gray: np.ndarray) -> np.ndarray:
    # Denoise
    denoised = cv2.fastNlMeansDenoising(gray, h=10)

    # CLAHE - improves contrast locally (great for uneven lighting)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)

    # Sharpen
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)

    return sharpened


# ─────────────────────────────────────────
# STEP 5: Binarization (clean black & white)
# ─────────────────────────────────────────
def binarize(image: np.ndarray) -> np.ndarray:
    # Adaptive threshold handles uneven illumination well
    binary = cv2.adaptiveThreshold(
        image, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=31,
        C=10
    )
    return binary


# ─────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────
def preprocess_pdf(pdf_path, output_dir="preprocessed_output"):
    os.makedirs(output_dir, exist_ok=True)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    print(f"\nProcessing: {pdf_path}")
    images = pdf_to_images(pdf_path, dpi=300)
    print(f"  Total pages: {len(images)}")

    preprocessed_pages = []

    for i, img in enumerate(images):
        print(f"  Page {i + 1}:")

        # Pipeline
        deskewed   = deskew(img)
        gray       = to_grayscale(deskewed)
        enhanced   = enhance_image(gray)
        binary     = binarize(enhanced)

        # Save each page
        out_path = os.path.join(output_dir, f"{pdf_name}_page_{i + 1}.png")
        cv2.imwrite(out_path, binary)
        print(f"  Saved → {out_path}")

        preprocessed_pages.append(binary)

    print(f"  Done! {len(preprocessed_pages)} pages saved to '{output_dir}/'")
    return preprocessed_pages


# ─────────────────────────────────────────
# RUN
# ─────────────────────────────────────────
preprocess_pdf("../digital_sample.pdf", output_dir="preprocessed_output/digital")
preprocess_pdf("../scanned_sample.pdf",  output_dir="preprocessed_output/scanned")