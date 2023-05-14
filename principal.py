import tkinter as tk
from tkinter import filedialog
import sys
import numpy as np
from PIL import Image
np.set_printoptions(threshold=sys.maxsize)


def open_second_window():
    resultadoD=''
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
    

  



# create the main window
root = tk.Tk()

# add widgets to main window
tk.Button(root, text="Metodo F5", command=open_second_window).pack()
tk.Button(root, text="Metodo LSB", command=open_second_window).pack()
tk.Button(root, text="Metodo Marca de Aguar", command=open_second_window).pack()





#METODO LSB 
#encoding function

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

#decoding function
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


root.mainloop()


