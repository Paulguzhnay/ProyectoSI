from PIL import Image, ImageDraw, ImageFont
import cv2

# Función para colocar una marca de agua en la imagen
def agregar_marca_agua(imagen, marca_agua):
    # Abre la imagen con PIL
    img = Image.open(imagen)
    
    # Crea una capa transparente para la marca de agua
    marca_agua_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    
    # Carga una fuente para el texto de la marca de agua
    fuente = ImageFont.truetype('arial.ttf', 50)
    
    # Dibuja el texto de la marca de agua en la capa transparente
    draw = ImageDraw.Draw(marca_agua_layer)
    draw.text((10, 10), marca_agua, font=fuente, fill=(255, 255, 255, 128))
    
    # Combina la imagen original con la capa de marca de agua
    imagen_con_marca_agua = Image.alpha_composite(img.convert('RGBA'), marca_agua_layer)
    
    # Guarda la imagen con la marca de agua
    imagen_con_marca_agua.save('imagen_con_marca_agua.png')
    
    # Muestra la imagen con la marca de agua
    imagen_con_marca_agua.show()

# Función para verificar si una imagen contiene la marca de agua
def verificar_marca_agua(imagen):
    # Carga la imagen con OpenCV
    img = cv2.imread(imagen)
    
    # Convierte la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Realiza una operación de umbralización para binarizar la imagen
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Busca la marca de agua en la imagen binarizada
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Verifica si se encontraron contornos en la imagen
    if len(contours) > 0:
        print("La imagen contiene la marca de agua.")
    else:
        print("La imagen no contiene la marca de agua.")

# Ejemplo de uso
agregar_marca_agua('imagen_original.jpg', 'Marca de Agua')
verificar_marca_agua('imagen_con_marca_agua.png')
