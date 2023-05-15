from PIL import Image

# Cargar la imagen
img = Image.open("_MG_0830 (1).JPG")

# Convertir la imagen a modo RGB
rgb_img = img.convert("RGB")

# Obtener los bits del mensaje a ocultar
hidden_message = "Hola Cruceta"
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
rgb_img.save("imagen_oculta.png")

def incrustarMarcaAgua():
    
