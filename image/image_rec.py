from PIL import Image
import pytesseract

# Load the uploaded image file
image_path = '/mnt/data/Screenshot 2024-12-19 at 11.03.47 AM.png'
image = Image.open(image_path)

# Use Tesseract to extract text from the image
extracted_text = pytesseract.image_to_string(image)
extracted_text