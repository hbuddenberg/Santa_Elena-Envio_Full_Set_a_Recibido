import os

import py7zr


def obtener_tamaño_total(archivos):
    tamaño_total = 0
    for archivo in archivos:
        tamaño_total += os.path.getsize(archivo) / (1024 * 1024)  # Convertir a MB
    return tamaño_total


def comprimir_archivos(archivos, archivo_7z, ruta_base):
    ruta_completa_7z = os.path.join(ruta_base, archivo_7z)
    with py7zr.SevenZipFile(ruta_completa_7z, "w") as archive:
        for archivo in archivos:
            ruta_completa = os.path.join(ruta_base, archivo)
            archive.write(ruta_completa, os.path.basename(ruta_completa))
    return archivo_7z


def validar_archivos(archivos, ruta_base, nombre_comprimido, tamaño_maximo=25):
    tamaño_total = obtener_tamaño_total([os.path.join(ruta_base, archivo) for archivo in archivos])
    if tamaño_total > tamaño_maximo:
        archivo_7z = f"{nombre_comprimido}.7z"
        archivo_comprimido = [comprimir_archivos(archivos, archivo_7z, ruta_base)]
        tamaño_comprimido = obtener_tamaño_total([os.path.join(ruta_base, archivo) for archivo in archivo_comprimido])
        return archivo_comprimido, tamaño_comprimido
    else:
        return archivos, tamaño_total
    # return archivos, tamaño_total


def main():
    asunto = (
        "FULL SET OF DOCS OE232400596 -OE232400597 -OE232400598 -OE232400599- MAERSK BULAN - TROPME (ETA 01-05-2024)"
    )
    ruta_base = "D:/Dev/Santa_Elena-Envio_Full_Set_a_Recibido/test/En Proceso/FULL SET OF DOCS OE232400596 -OE232400597 -OE232400598 -OE232400599- MAERSK BULAN - TROPME (ETA 01-05-2024)"
    archivos = [
        "FULL SET OE232400596- MAERSK BULAN - TROPME-1.pdf ",
        "FULL SET OE232400596- MAERSK BULAN - TROPME.pdf ",
        "FULL SET OE232400597- MAERSK BULAN - TROPME.pdf ",
        "PACKING LIST  - OE232400597_MAERSK BULAN_TROPME.xls ",
        "PACKING LIST - OE232400598_MAERSK BULAN_TROPME.xls ",
        "PACKING LIST - OE232400599_MAERSK BULAN_TROPME.xls",
    ]
    archivos_validados, tamaño_total = validar_archivos(archivos, ruta_base, asunto)
    print(f"Archivos a enviar: {archivos_validados}")


if __name__ == "__main__":
    main()
