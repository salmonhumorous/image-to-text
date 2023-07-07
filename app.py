import os


path = os.getcwd()+'/templates'
try:os.mkdir(path)
except:pass
with open(os.path.join(path, 'index.html'), 'w') as fp:
  fp.write('''<html>
<head>
    <title>Extract data</title>
</head>
<body>
    <p>Convert Image to text</p>
    <form action = "/success-image" method = "post" enctype="multipart/form-data">
        <input type="file" name="file" required/>
        <input type = "submit" value="Upload">
    </form>
    <p>Convert Pdf to text</p>
    <form action = "/success-pdf" method = "post" enctype="multipart/form-data">
        <input type="file" name="file" required/>
        <input type = "submit" value="Upload">
    </form>
</body>
</html>''')

with open(os.path.join(path, 'acknowledgement.html'), 'w') as fp:
  fp.write('''<html>
<head>
    <title>success</title>
</head>
<body>
    <p>File uploaded successfully</p>
    <p>Text Extracted: {{text}}</p>
</body>
</html>''')

"""# **Function to convert image into extracted data**"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

#tesseract path on the machine (imp)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Path of working folder on Disk

def extract_text_from_image(img_path):
    # Read image with opencv
    img = cv2.imread(img_path)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write image after removed noise
    # cv2.imwrite("removed_noise.png", img)

    #  Apply threshold to get image with only black and white
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    # cv2.imwrite(img_path, img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(img_path))

    # Remove template file
    #os.remove(temp)

    return result

def extract_text_from_pdf(pdf_path):
   # Convert PDF to image
    pages = convert_from_path(pdf_path, 500)
     
    # Extract text from each page using Tesseract OCR
    text_data = ''
    seperator = '----------------------------------------------------------------------------------------------------'
    for page in pages:
        text = pytesseract.image_to_string(page)
        text_data += text + '\n' + seperator + '\n'
     
    # Return the text data
    return text_data
    



"""# **Flask server to convert to upload image and extract information**"""


from flask import *
app = Flask(__name__)

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/success-image', methods = ['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        text = extract_text_from_image(f.filename)
        os.remove(f.filename)
        return render_template("acknowledgement.html", text = text)
    
@app.route('/success-pdf', methods = ['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        text = extract_text_from_pdf(f.filename)
        os.remove(f.filename)
        return render_template("acknowledgement.html", text = text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
