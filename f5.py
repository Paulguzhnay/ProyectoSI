import hashlib
from PIL import Image
from Crypto.Cipher import AES
import os

# Algoritmo F5 para ocultar el mensaje en la imagen de cubierta
def f5_encode(img_path, message, key, threshold=0.1):
    img = Image.open(img_path)
    pixels = img.load()
    width, height = img.size
    block_size = 8
    block_area = block_size * block_size
    
    # Convertir el mensaje a una secuencia de bits y encriptarla
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    # message = cipher.encrypt(message)
    message, tag = cipher.encrypt_and_digest(message)    
    message_bits = [int(b) for b in ''.join(['{:08b}'.format(x) for x in message])]
    
    # Ocultar los bits del mensaje en la imagen de cubierta
    block_means = []
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            block_pixels = []
            for i in range(block_size):
                for j in range(block_size):
                    if x+j < width and y+i < height:
                        block_pixels.append(pixels[x+j,y+i])
            block_mean = sum([sum(p)/len(p) for p in block_pixels]) / block_area
            block_means.append((block_mean, (x, y)))
    
    block_means = sorted(block_means)
    bits_written = 0
    for i in range(len(block_means)-1):
        block1_mean, block1_pos = block_means[i]
        block2_mean, block2_pos = block_means[i+1]
        diff = abs(block2_mean - block1_mean)
        if diff > threshold and bits_written < len(message_bits):
            for j in range(block_area):
                if bits_written >= len(message_bits):
                    break
                x = block1_pos[0] + (j % block_size)
                y = block1_pos[1] + (j // block_size)
                pixel = list(pixels[x,y])
                bit = message_bits[bits_written]
                if bit == 0:
                    if pixel[-1] % 2 == 1:
                        pixel[-1] -= 1
                else:
                    if pixel[-1] % 2 == 0:
                        pixel[-1] += 1
                pixels[x,y] = tuple(pixel)
                bits_written += 1
        elif bits_written >= len(message_bits):
            break
    
    img.save(os.path.splitext(img_path)[0] + '_encoded.png', 'PNG')
    return (nonce)



def f5_decode(img_path, key, nonce1, tag, threshold=0.1):
    img = Image.open(img_path)
    pixels = img.load()
    width, height = img.size
    block_size = 8
    block_area = block_size * block_size

    # Obtener los bits del mensaje oculto
    block_means = []
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            block_pixels = []
            for i in range(block_size):
                for j in range(block_size):
                    if x+j < width and y+i < height:
                        block_pixels.append(pixels[x+j,y+i])
            block_mean = sum([sum(p)/len(p) for p in block_pixels]) / block_area
            block_means.append((block_mean, (x, y)))
    
    block_means = sorted(block_means)
    message_bits = []
    for i in range(len(block_means)-1):
        block1_mean, block1_pos = block_means[i]
        block2_mean, block2_pos = block_means[i+1]
        diff = abs(block2_mean - block1_mean)
        if diff > threshold:
            for j in range(block_area):
                x = block1_pos[0] + (j % block_size)
                y = block1_pos[1] + (j // block_size)
                pixel = list(pixels[x,y])
                bit = pixel[-1] % 2
                message_bits.append(bit)
    
    # Convertir los bits del mensaje a bytes y desencriptarlos
    message_bytes = bytearray()
    for i in range(0, len(message_bits), 8):
        message_byte = 0
        for j in range(8):
            message_byte = (message_byte << 1) | message_bits[i+j]
        message_bytes.append(message_byte)
    
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce1)
    message = cipher.decrypt(message_bytes)    
    return message

# clave='SuperClave123'
# # clave=clave.encode()
# # clave = clave + b'\0' * (16 - len(clave))
# # print(clave)

# key = clave.encode()
# key = key + b'\0' * (16 - len(key))
# print(key)

# cover_image = 'odlzjiuaivudywp4.jpg'
# mensaje='el hippie josephdawdwa'
# message = mensaje.encode()
# bytesmessage=len(message)

# # Codificar mensaje en la imagen
# messageencrypt, nonce, tag = f5_encode(cover_image, message, key)

# # Guardar la imagen con el mensaje oculto
# hidden_image = 'odlzjiuaivudywp4_encoded.png'

# # Decodificar mensaje de la imagen
# message = f5_decode(hidden_image, key, nonce, tag)
# text = message[:bytesmessage]
# print(text)

