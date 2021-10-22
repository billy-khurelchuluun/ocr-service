from flask import Flask, jsonify, make_response, request
from PIL import Image
from io import BytesIO
import requests
import os
import simplejson as json
import pytesseract
import pdf2image

app = Flask("OCR Service")

@app.route("/", methods=['GET'])
def hello():
    return "Hello OCR"


@app.route("/parse", methods=['POST'])
def parseImage():
    req = request.get_json()
    if 'url' not in req:
        return 'url not provided', 400
    if 'docType' not in req:
        return 'docType not provided', 400

    url = req['url']
    doctype = req['docType']
    crop = False
    box = []

    if 'crop' in req and req['crop'] == True:
        boxStr = req['cropBox'].split(',')
        box = [int(s) for s in boxStr]
        crop = True


    if doctype=='image':
        img = getImageFromUrl(url)
        if crop:
            img = cropImage(img, box)
        return parseImage(img)
    elif doctype=='pdf':
        return parseFromPdf(url, crop, box)
    else:
        return 'docType not supported.', 400


def getImageFromUrl(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    with open('parsed.jpg', 'w+b') as f:
         f.write(BytesIO(response.content).getvalue()) # pdf type is bytes by default
    return img


def parseImage(img):
    results = "";
    results +=  pytesseract.image_to_string(img, lang='eng')
    results += "\n" + pytesseract.image_to_data(img, lang='eng')
    return results


def cropImage(img, box):
    return img.crop(box)

#194,411, 456,456
def parseFromPdf(url, crop, box):
    result = ""
    pages = pdf2image.convert_from_path(url)
#    pdfBytes = requests.get(url).raw.read()
#    pages = pdf2image.convert_from_bytes(pdfBytes)
    for pg, img in enumerate(pages):

         if crop:
             img = img.crop( box )
         result += pytesseract.image_to_string(img, lang='eng')
         with open('parsed.jpg', 'w+b') as f:
            img_bytes = BytesIO()
            img.save(img_bytes, format='PNG')
            f.write(img_bytes.getvalue())
    return result


if __name__ == '__main__':
    app.run(port=5000, debug=True)
