import os
from PIL import Image, ImageDraw, ImageFont

def draw_grid(image_path):
    # Apri l'immagine originale
    original_image = Image.open(image_path)

    # Ottieni la risoluzione dell'immagine in DPI (punti per pollice)
    dpi = original_image.info.get('dpi')

    # Calcola il numero di pixel per centimetro in base ai DPI
    pixels_per_cm = dpi[0] / 2.54

    # Calcola la dimensione in pixel per 16 cm
    size_in_pixel = int(pixels_per_cm * 16)

    # Crea una nuova immagine con la dimensione calcolata
    new_image = Image.new('RGB', (size_in_pixel, size_in_pixel), 'white')

    # Ridimensiona l'immagine originale alla dimensione desiderata
    resized_image = original_image.resize((size_in_pixel, size_in_pixel))

    # Copia l'immagine ridimensionata nella nuova immagine
    new_image.paste(resized_image, (0, 0))

    # Crea un oggetto ImageDraw per disegnare sulla nuova immagine
    draw = ImageDraw.Draw(new_image)

    # Calcola la dimensione di ciascun quadratino
    square_size = size_in_pixel // 16

    # Imposta lo spessore e il colore dei tratti e dei numeri
    line_width = 5
    line_color = 'red'
    font_size = font_size = int(pixels_per_cm * 0.4)

    # Carica un font con la dimensione desiderata
    font = ImageFont.truetype("arial.ttf", font_size)

    # Disegna la griglia con numerazione
    for i in range(16):
        for j in range(16):
            x = j * square_size
            y = (15 - i) * square_size
            draw.line([(x, 0), (x, size_in_pixel)], fill=line_color, width=line_width)
            draw.line([(0, y), (size_in_pixel, y)], fill=line_color, width=line_width)
            draw.text((x + 2, y + 2), f'{j},{i}', fill=line_color, font=font)  # Scambia j con i

    # Ottieni il percorso dell'immagine di origine
    image_dir = os.path.dirname(image_path)

    # Salva l'immagine risultante nella stessa cartella dell'immagine di origine
    new_image_path = os.path.join(image_dir, 'immagine_con_griglia.png')
    new_image.save(new_image_path)
    print(f"L'immagine con la griglia è stata salvata come: {new_image_path}")

# Richiedi il percorso dell'immagine da tastiera
input_image_path = input("Inserisci il percorso dell'immagine: ")
draw_grid(input_image_path)
