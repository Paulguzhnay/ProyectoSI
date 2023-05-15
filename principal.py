import tkinter as tk
from tkinter import filedialog
import sys
import numpy as np
from PIL import Image
np.set_printoptions(threshold=sys.maxsize)
import hashlib
from PIL import Image
from Crypto.Cipher import AES
import os


noncef5=''
bytesmessage=0

def open_first_window():
    resultadoD=''
    second_window = tk.Toplevel(root)

    # add widgets to second window
    tk.Label(second_window, text="Ruta Imagen Original F5").grid(row=0, column=0)
    rutaImgOriginalTexto = tk.Entry(second_window)
    rutaImgOriginalTexto.grid(row=0, column=1)
    
    def select_image():
        rutaImagenOriginal = filedialog.askopenfilename()
        rutaImgOriginalTexto.delete(0, tk.END)
        rutaImgOriginalTexto.insert(0, rutaImagenOriginal)
        print("Imagen seleccionada:", rutaImagenOriginal)
        
    tk.Button(second_window, text="Seleccionar imagen", command=select_image).grid(row=1, column=1)
    
    tk.Label(second_window).grid(row=2, column=0)
    tk.Label(second_window, text="Mensaje a encriptar").grid(row=3, column=0)
    message_entry = tk.Entry(second_window)
    message_entry.grid(row=3, column=1)
    
    tk.Label(second_window).grid(row=4, column=0)
    tk.Label(second_window, text="Clave para encriptar").grid(row=4, column=0)
    clave = tk.Entry(second_window, show="*")
    clave.grid(row=4, column=1)
    
    # tk.Label(second_window).grid(row=5, column=0)
    # tk.Label(second_window, text="Nombre Imagen Encriptada").grid(row=5, column=0)
    # rutaImgFinalTexto = tk.Entry(second_window)
    # rutaImgFinalTexto.grid(row=5, column=1)
    # tk.Label(second_window).grid(row=6, column=0)
    #-----------------------------------------------------------------------------------
    tk.Label(second_window, text="Clave para desencriptar").grid(row=4, column=4)
    claveD = tk.Entry(second_window, show="*")
    claveD.grid(row=4, column=5)
    
    tk.Label(second_window, text="Nombre Imagen Encriptada").grid(row=5, column=4)
    rutaImgOriginalTextoD = tk.Entry(second_window)
    rutaImgOriginalTextoD.grid(row=5, column=5)


    def select_imageD():
        rutaImagenOriginal = filedialog.askopenfilename()
        rutaImgOriginalTextoD.delete(0, tk.END)
        rutaImgOriginalTextoD.insert(0, rutaImagenOriginal)
        print("Imagen seleccionada:", rutaImagenOriginal)


    tk.Button(second_window, text="Seleccionar imagen", command=select_imageD).grid(row=6, column=4)
    
    def encriptar():
        rutaImgOriginal = rutaImgOriginalTexto.get()
        mensaje = message_entry.get()
        claveF = clave.get()
        message=mensaje.encode()
        global bytesmessage
        bytesmessage=len(message)
        key=claveF.encode()
        key = key + b'\0' * (16 - len(key))
        # rutaImgFinal = rutaImgFinalTexto.get()
        print(mensaje)
        print(claveF)
        # print(rutaImgFinal)
        # Encriptar(rutaImgOriginal,mensaje,rutaImgFinal,claveF)
        global noncef5
        noncef5=f5_encode(rutaImgOriginal,message,key)
        second_window.destroy()

    def desencriptar():
        rutaImgDesc = rutaImgOriginalTextoD.get()
        claveDF = claveD.get()
        key=claveDF.encode()
        key = key + b'\0' * (16 - len(key))
        print(claveD)
        print(rutaImgDesc)
        resultado=f5_decode(rutaImgDesc,key,noncef5,tag=0)
        resultado = resultado[:bytesmessage]
        print("texto descifrado", resultado)
        # resultadoD=Desencriptar(rutaImgDesc,claveDF)
        tk.Label(second_window, text="Texto Oculto").grid(row=8, column=4)
        tk.Label(second_window, text=resultado).grid(row=9, column=4)    


    tk.Button(second_window, text="Encriptar", command=encriptar).grid(row=7, column=1)
    tk.Button(second_window, text="Desencriptar", command=desencriptar).grid(row=7, column=4)
    

def open_second_window():

    second_window = tk.Toplevel(root)

    # add widgets to second window
    tk.Label(second_window, text="Ruta Imagen Original").grid(row=0, column=0)
    rutaImgOriginalTexto = tk.Entry(second_window)
    rutaImgOriginalTexto.grid(row=0, column=1)
    
    def select_image():
        rutaImagenOriginal = filedialog.askopenfilename()
        rutaImgOriginalTexto.delete(0, tk.END)
        rutaImgOriginalTexto.insert(0, rutaImagenOriginal)
        print("Imagen seleccionada:", rutaImagenOriginal)
        
    tk.Button(second_window, text="Seleccionar imagen", command=select_image).grid(row=1, column=1)
    
    tk.Label(second_window).grid(row=2, column=0)
    tk.Label(second_window, text="Mensaje a encriptar").grid(row=3, column=0)
    message_entry = tk.Entry(second_window)
    message_entry.grid(row=3, column=1)
    
    tk.Label(second_window).grid(row=4, column=0)
    tk.Label(second_window, text="Clave para encriptar").grid(row=4, column=0)
    clave = tk.Entry(second_window, show="*")
    clave.grid(row=4, column=1)
    
    tk.Label(second_window).grid(row=5, column=0)
    tk.Label(second_window, text="Nombre Imagen Encriptada").grid(row=5, column=0)
    rutaImgFinalTexto = tk.Entry(second_window)
    rutaImgFinalTexto.grid(row=5, column=1)
    tk.Label(second_window).grid(row=6, column=0)
    #-----------------------------------------------------------------------------------
    tk.Label(second_window, text="Clave para desencriptar").grid(row=4, column=4)
    claveD = tk.Entry(second_window, show="*")
    claveD.grid(row=4, column=5)
    
    tk.Label(second_window, text="Nombre Imagen Encriptada").grid(row=5, column=4)
    rutaImgOriginalTextoD = tk.Entry(second_window)
    rutaImgOriginalTextoD.grid(row=5, column=5)


    def select_imageD():
        rutaImagenOriginal = filedialog.askopenfilename()
        rutaImgOriginalTextoD.delete(0, tk.END)
        rutaImgOriginalTextoD.insert(0, rutaImagenOriginal)
        print("Imagen seleccionada:", rutaImagenOriginal)


    tk.Button(second_window, text="Seleccionar imagen", command=select_imageD).grid(row=6, column=4)
    
    def encriptar():
        rutaImgOriginal = rutaImgOriginalTexto.get()
        mensaje = message_entry.get()
        claveF = clave.get()
        rutaImgFinal = rutaImgFinalTexto.get()
        print(mensaje)
        print(claveF)
        print(rutaImgFinal)
        Encriptar(rutaImgOriginal,mensaje,rutaImgFinal,claveF)
        second_window.destroy()

    def desencriptar():
        rutaImgDesc = rutaImgOriginalTextoD.get()
        claveDF = claveD.get()
        print(claveD)
        print(rutaImgDesc)
        resultadoD=Desencriptar(rutaImgDesc,claveDF)
        tk.Label(second_window, text="Texto Oculto").grid(row=8, column=4)
        tk.Label(second_window, text=resultadoD).grid(row=9, column=4)    


    tk.Button(second_window, text="Encriptar", command=encriptar).grid(row=7, column=1)
    tk.Button(second_window, text="Desencriptar", command=desencriptar).grid(row=7, column=4)
    

  

def open_third_window():

    third_window = tk.Toplevel(root)

    # add widgets to third window
    tk.Label(third_window, text="Ruta Imagen Original").grid(row=0, column=0)
    rutaImgOriginalTexto = tk.Entry(third_window)
    rutaImgOriginalTexto.grid(row=0, column=1)
    
    def select_image():
        rutaImagenOriginal = filedialog.askopenfilename()
        rutaImgOriginalTexto.delete(0, tk.END)
        rutaImgOriginalTexto.insert(0, rutaImagenOriginal)
        print("Imagen seleccionada:", rutaImagenOriginal)
        
    tk.Button(third_window, text="Seleccionar imagen", command=select_image).grid(row=1, column=1)
    
    tk.Label(third_window).grid(row=2, column=0)
    tk.Label(third_window, text="Mensaje para la marca de agua").grid(row=3, column=0)
    message_entry = tk.Entry(third_window)
    message_entry.grid(row=3, column=1)
    

    
    tk.Label(third_window).grid(row=5, column=0)
    tk.Label(third_window, text="Nombre Imagen Encriptada").grid(row=5, column=0)
    rutaImgFinalTexto = tk.Entry(third_window)
    rutaImgFinalTexto.grid(row=5, column=1)
    tk.Label(third_window).grid(row=6, column=0)
    #-----------------------------------------------------------------------------------
    tk.Label(third_window, text="Mensaje para la marca de agua").grid(row=4, column=4)
    claveD = tk.Entry(third_window, show="*")
    claveD.grid(row=4, column=5)
    
    tk.Label(third_window, text="Nombre Imagen Encriptada").grid(row=5, column=4)
    rutaImgOriginalTextoD = tk.Entry(third_window)
    rutaImgOriginalTextoD.grid(row=5, column=5)


    def select_imageD():
        rutaImagenOriginal = filedialog.askopenfilename()
        rutaImgOriginalTextoD.delete(0, tk.END)
        rutaImgOriginalTextoD.insert(0, rutaImagenOriginal)
        print("Imagen seleccionada:", rutaImagenOriginal)


    tk.Button(third_window, text="Seleccionar imagen", command=select_imageD).grid(row=6, column=4)
    
    def encriptar():
        rutaImgOriginal = rutaImgOriginalTexto.get()
        mensaje = message_entry.get()
     
        rutaImgFinal = rutaImgFinalTexto.get()
        print(mensaje)

        print(rutaImgFinal)
        incrustarMarca(rutaImgOriginal, mensaje, rutaImgFinal)
        third_window.destroy()

    def desencriptar():
        rutaImgDesc = rutaImgOriginalTextoD.get()
        claveDF = claveD.get()
        print(claveD)
        print(rutaImgDesc)
        resultadoD= verificarMarca(rutaImgDesc, claveDF)
        tk.Label(third_window, text="Texto Oculto").grid(row=8, column=4)
        tk.Label(third_window, text=resultadoD).grid(row=9, column=4)    


    tk.Button(third_window, text="Incrustar", command=encriptar).grid(row=7, column=1)
    tk.Button(third_window, text="Verificar", command=desencriptar).grid(row=7, column=4)
      



# create the main window
root = tk.Tk()

# add widgets to main window
tk.Button(root, text="Metodo F5", command=open_first_window).pack()
tk.Button(root, text="Metodo LSB", command=open_second_window).pack()
tk.Button(root, text="Metodo Marca de Agua", command=open_third_window).pack()





#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------LSB---------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------

def Encriptar(rutaImgOrig, mensaje, rutaImgFinal,clave):
    #texto=eval(rutaImgFinal)
    textoFinal=rutaImgFinal.split()[0]
    #rutaImgFinal=rutaImgFinal.split()[0]
    print(len(textoFinal))
    print(textoFinal,".png")

    img = Image.open(rutaImgOrig, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size//n

    mensaje += clave
    b_mensaje = ''.join([format(ord(i), "08b") for i in mensaje])
    req_pixels = len(b_mensaje)

    if req_pixels > (total_pixels * 3):
        print("ERROR: Need larger file size")

    else:
        index=0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_mensaje[index], 2)
                    index += 1

        array=array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(rutaImgFinal.lower()+".png")
        
        print("Imagen Encriptada")


def Desencriptar(rutaImg, claveD):

    img = Image.open(rutaImg, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size//n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    hiddenmessage = ""
    for i in range(len(hidden_bits)):
        x = len(claveD)
        if message[-x:] == claveD:
            break
        else:
            message += chr(int(hidden_bits[i], 2))
            message = f'{message}'
            hiddenmessage = message
    #verifying the claveD
    if claveD in message:
        print("Mensaje Oculto:", hiddenmessage[:-x])
        return hiddenmessage[:-x]
    else:
        print("claveD incorrecta")


#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------F5----------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
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




#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------Marca de Agua-----------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------



def incrustarMarca(imagen, mensaje, nuevaImagen):
    img = Image.open(imagen)

    # Convertir la imagen a modo RGB
    rgb_img = img.convert("RGB")

    # Obtener los bits del mensaje a ocultar
    hidden_message = mensaje
    message_bits = ''.join(format(ord(c), '08b') for c in hidden_message)

    # Verificar que la imagen tenga suficientes píxeles para almacenar el mensaje
    required_pixels = len(message_bits) // 3
    if required_pixels > rgb_img.width * rgb_img.height:
        print("La imagen es demasiado pequeña para ocultar el mensaje.")
        exit()

    # Ocultar los bits del mensaje en los bits menos significativos de los componentes rojo, verde y azul de los píxeles
    bit_counter = 0
    for y in range(rgb_img.height):
        for x in range(rgb_img.width):
            r, g, b = rgb_img.getpixel((x, y))
            if bit_counter < len(message_bits):
                r = int(bin(r)[:-1] + message_bits[bit_counter], 2)
                bit_counter += 1
            if bit_counter < len(message_bits):
                g = int(bin(g)[:-1] + message_bits[bit_counter], 2)
                bit_counter += 1
            if bit_counter < len(message_bits):
                b = int(bin(b)[:-1] + message_bits[bit_counter], 2)
                bit_counter += 1
            rgb_img.putpixel((x, y), (r, g, b))

    # Guardar la imagen con el mensaje oculto
    rgb_img.save(os.path.splitext(nuevaImagen)[0] + '.png', 'PNG')


def verificarMarca(imagen, mensaje):
    # Carga la imagen
    img = Image.open(imagen)

    # Convierte la imagen a modo RGB
    rgb_img = img.convert("RGB")

    # Obtiene las dimensiones de la imagen
    width, height = rgb_img.size

    # Extrae los bits menos significativos de cada componente rojo, verde y azul de los píxeles
    bit_sequence = ''
    for y in range(height):
        for x in range(width):
            r, g, b = rgb_img.getpixel((x, y))
            bit_sequence += bin(r)[-1] + bin(g)[-1] + bin(b)[-1]

    # Verifica si el mensaje está presente en la imagen
    message_to_check = mensaje
    bit_sequence_to_check = ''
    for char in message_to_check:
        bit_sequence_to_check += bin(ord(char))[2:].zfill(8)

    print(len(bit_sequence))

    if bit_sequence_to_check in bit_sequence:
        return ('El mensaje está presente en la imagen.')
    else:
        return ('El mensaje no está presente en la imagen.')

root.mainloop()


