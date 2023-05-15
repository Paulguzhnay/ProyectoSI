from PIL import Image

# Carga la imagen
img = Image.open("imagen_oculta.png")

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
message_to_check = "Hola Cruceta"
bit_sequence_to_check = ''
for char in message_to_check:
    bit_sequence_to_check += bin(ord(char))[2:].zfill(8)

print(len(bit_sequence))

if bit_sequence_to_check in bit_sequence:
    print('El mensaje está presente en la imagen.')
else:
    print('El mensaje no está presente en la imagen.')

'''import hashlib
from PIL import Image

# Cargar la imagen
img = Image.open("imagen_oculta.png")

# Convertir la imagen a modo RGB
rgb_img = img.convert("RGB")

# Extraer los bits menos significativos de cada componente rojo, verde y azul de los píxeles
bit_sequence = ''
for y in range(rgb_img.height):
    for x in range(rgb_img.width):
        r, g, b = rgb_img.getpixel((x, y))
        bit_sequence += bin(r)[-1] + bin(g)[-1] + bin(b)[-1]

# Obtener el hash SHA-256 del mensaje oculto
hidden_message = "Hola Cruceta"
message_hash = hashlib.sha256(hidden_message.encode()).hexdigest()

print(bit_sequence)

# Verificar si el hash del mensaje oculto está presente en la secuencia de bits de la imagen
if message_hash in bit_sequence:
    print("El mensaje oculto está presente en la imagen.")
else:
    print("El mensaje oculto no está presente en la imagen.")
'''