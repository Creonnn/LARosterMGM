from pytesseract import pytesseract
from PIL import Image
import urllib.request

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def convert(URL):
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', '')
    filename, headers = opener.retrieve(URL, 'temp.png')
    img = Image.open(filename)

    class_name_text = pytesseract.image_to_string(crop_class_name(img)).split()[0]
    char_name_text = pytesseract.image_to_string(crop_char_name(img)).split()[0]
    ilvl_text = pytesseract.image_to_string(crop_ilvl(img)).split()[0]

    return class_name_text, char_name_text, ilvl_text


def crop_class_name(img):
    left = 150
    top = 135
    right = 300
    bottom = 170
    class_name_img = img.crop((left, top, right, bottom))
    class_name_img.save('class_name.png')
    return class_name_img

def crop_char_name(img):
    left = 115
    top = 170
    right = 345
    bottom = 200
    char_name_img = img.crop((left, top, right, bottom))
    char_name_img.save('char_name.png')
    return char_name_img

def crop_ilvl(img):
    left = 910
    top = 230
    right = 1000
    bottom = 260
    ilvl_img = img.crop((left, top, right, bottom))
    ilvl_img.save('ilvl.png')
    return ilvl_img

