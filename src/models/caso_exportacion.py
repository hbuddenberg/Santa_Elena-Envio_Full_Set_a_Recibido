class CasoExportacion:
    def __init__(self, pais='', emails_para='', emails_copia='', adjuntos='', asunto='', cuerpo=''):
        self.pais = pais
        self.emails_para = emails_para
        self.emails_copia = emails_copia
        self.adjuntos = adjuntos
        self.asunto = asunto
        self.cuerpo = cuerpo

    def __repr__(self):
        return (f"CasoExportacion(pais={self.pais}, emails_para={self.emails_para}, "
                f"emails_copia={self.emails_copia}, adjuntos={self.adjuntos}, "
                f"asunto={self.asunto}, cuerpo={self.cuerpo})")

    def to_dict(self):
        return {
            'pais': self.pais,
            'emails_para': self.emails_para,
            'emails_copia': self.emails_copia,
            'adjuntos': self.adjuntos,
            'asunto': self.asunto,
            'cuerpo': self.cuerpo
        }

# Ejemplo de uso
caso = CasoExportacion(
    pais='España',
    emails_para='example@example.com',
    emails_copia='cc@example.com',
    adjuntos='documento.pdf',
    asunto='Asunto del correo',
    cuerpo='Cuerpo del correo'
)

print(caso)
print(caso.to_dict())