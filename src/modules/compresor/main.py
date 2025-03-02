import os
import zipfile

def obtener_tamaño_total(archivos):
    tamaño_total = 0
    for archivo in archivos:
        tamaño_total += os.path.getsize(archivo) / (1024 * 1024)  # Convertir a MB
    return tamaño_total

def comprimir_archivos(archivos, archivo_zip, ruta_base):
    ruta_completa_zip = os.path.join(ruta_base, archivo_zip)
    with zipfile.ZipFile(ruta_completa_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for archivo in archivos:
            ruta_completa = os.path.join(ruta_base, archivo)
            zipf.write(ruta_completa, os.path.basename(ruta_completa))
    return archivo_zip

def validar_archivos(archivos, ruta_base, nombre_comprimido, tamaño_maximo=25):
    tamaño_total = obtener_tamaño_total([os.path.join(ruta_base, archivo) for archivo in archivos])
    if tamaño_total > tamaño_maximo:
        archivo_zip = f'{nombre_comprimido}.zip'
        return [comprimir_archivos(archivos, archivo_zip, ruta_base)], tamaño_total
    else:
        return archivos, tamaño_total

def main():
    asunto = 'FULL SET OF DOCS OE232400596 -OE232400597 -OE232400598 -OE232400599- MAERSK BULAN - TROPME (ETA 01-05-2024)'
    ruta_base = '/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/test/En Proceso/FULL SET OF DOCS OE232400596 -OE232400597 -OE232400598 -OE232400599- MAERSK BULAN - TROPME (ETA 01-05-2024)'  # Ajusta esta ruta según tus necesidades
    archivos = ['FULL SET OE232400596- MAERSK BULAN - TROPME-1.pdf', 'FULL SET OE232400596- MAERSK BULAN - TROPME.pdf']
    archivos_validados, tamaño_total = validar_archivos(archivos, ruta_base, asunto)
    print(f"Archivos a enviar: {archivos_validados}")

if __name__ == "__main__":
    main()