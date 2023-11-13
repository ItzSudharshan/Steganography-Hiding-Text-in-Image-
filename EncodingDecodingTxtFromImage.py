from PIL import Image
import getpass
import sys

def print_header():
    print("****************************************")
    print("**        Welcome to Steganography    **")
    print("****************************************")

def genData(data):
    newd = [format(ord(i), '08b') for i in data]
    return newd

def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        for j in range(0, 8):
            if datalist[i][j] == '0' and pix[j] % 2 != 0:
                pix[j] -= 1
            elif datalist[i][j] == '1' and pix[j] % 2 == 0:
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[j] += 1

        if i == lendata - 1:
            if pix[-1] % 2 == 0:
                if pix[-1] != 0:
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if pix[-1] % 2 != 0:
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data, key):
    # Adding key to the data for encoding
    data = key + " " + data
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1

def encode():
    print_header()
    img_name = input("Enter image name (with extension): ")
    
    try:
        image = Image.open(img_name, 'r')
    except FileNotFoundError:
        print(f"Error: Image '{img_name}' not found. Please check the file path and try again.")
        sys.exit()

    key = getpass.getpass("Enter key for encoding: ")
    data = input("Enter data to be encoded: ")
    if len(data) == 0:
        raise ValueError('Data is empty')

    newimg = image.copy()
    encode_enc(newimg, data, key)

    new_img_name = input("Enter the name of the new image (with extension): ")
    
    # Get the format from the new image name
    img_format = new_img_name.split(".")[-1].upper()
    
    newimg.save(new_img_name, format=img_format)
    
    print("Encoding successful! Exiting program.")
    sys.exit()

def decode():
    print_header()
    img_name = input("Enter The image name (with extension) to be Decoded: ")
    
    try:
        image = Image.open(img_name, 'r')
    except FileNotFoundError:
        print(f"Error: Image '{img_name}' not found. Please check the file path and try again.")
        sys.exit()

    key = getpass.getpass("Enter key for decoding: ")
    data = ''
    imgdata = iter(image.getdata())

    while True:
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        binstr = ''

        for i in pixels[:8]:
            if i % 2 == 0:
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if pixels[-1] % 2 != 0:
            break

    # Splitting the data into key and actual data
    stored_key, actual_data = data.split(" ", 1)

    # Verify key before returning the decoded data
    if key == stored_key:
        return actual_data
    else:
        raise ValueError("Incorrect key")

def main():
    a = int(input("1. Encode\n2. Decode\n"))
    if a == 1:
        encode()
    elif a == 2:
        try:
            decoded_data = decode()
            print("Decoded Text:", decoded_data)
        except ValueError as e:
            print(e)
    else:
        raise Exception("Enter correct input")

if __name__ == '__main__':
    main()
