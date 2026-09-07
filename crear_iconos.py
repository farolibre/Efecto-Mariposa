from PIL import Image, ImageDraw, ImageFont

def crear_icono(tamaño, nombre):
    # Crear imagen con fondo morado
    img = Image.new('RGB', (tamaño, tamaño), '#6C63FF')
    draw = ImageDraw.Draw(img)
    
    # Dibujar un círculo interior
    margen = tamaño // 8
    draw.ellipse([margen, margen, tamaño-margen, tamaño-margen], fill='#764ba2')
    
    # Dibujar la mariposa
    try:
        font = ImageFont.truetype("segoeui.ttf", tamaño//2)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", tamaño//2)
        except:
            font = ImageFont.load_default()
    
    draw.text((tamaño//2, tamaño//2), "🦋", fill='white', anchor='mm', font=font)
    
    # Guardar
    img.save(f'static/{nombre}')
    print(f'✅ {nombre} creado')

# Crear ambos iconos
crear_icono(192, 'icon-192.png')
crear_icono(512, 'icon-512.png')
print('🎉 ¡Iconos creados correctamente!')