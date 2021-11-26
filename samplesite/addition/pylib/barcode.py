import random
import barcode
from barcode.writer import ImageWriter


def generate_barcode(id_cat, id_type_material, title_material):
    randomNum = random.uniform(10000000, 99999999)
    number_ean = (id_cat, id_type_material, randomNum)
    float_number = float(''.join(map(str, number_ean)))
    EAN = barcode.get('ean13', f'{float_number}', writer=ImageWriter())
    filename = EAN.save(title_material)
    get_data = [float_number, filename]
    get_data[0] = float_number
    get_data[1] = filename
    return get_data

# def read_barcode():
#     image_barcode = image.open('barcode.png')
#     decoded = decode(image_barcode)
#     get_data1 = [decoded]
#     get_data1[0] = decoded
#     return get_data1
