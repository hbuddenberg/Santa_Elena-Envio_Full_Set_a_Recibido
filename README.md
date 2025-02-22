# Envio Full Set a Recibidor

-----

1. Obtener carpetas existentes en raiz
2. Moverlas a "En Proceso"
3. Obtener listado de carpetas a procesar.
4. Se obtendra extracción del Excel de "Configuracion de Envio".
   - Pestaña:
     - DISTRIBUCION CORREOS
     - RECIBIDORES EMAILS
     - RESUMEN CC
     - EMAIL REPORTE
5. Por cada carpeta:
   1. Se obtendra el nombre de la carpeta:
      - El nombre de la carpeta funcionara como nombre de Asunto.
      - Del nombre del asunto se obtendra el nombre del Recibidor.
   2. Mediante el nombre del recibidor:
      - Desde el Excel de "Configuracion de Envio", pestaña "RECIBIDORES EMAILS", se obtendra los correos de destinatarios y el "Flag de Distribución".
      - Mediante el "Flag de Distribución", desde el Excel de "Configuracion de Envio", pestaña "DISTRIBUCION CORREOS", se obtendra el registro relacionado al "Caso de Envio".
      - Desde el Excel de "Configuracion de Envio", pestaña "RESUMEN CC", se obtendra los correos de copia.
      - Desde el Excel de "Configuracion de Envio", pestaña "EMAIL REPORTE", se obtendra los correos de el envio del reporte una vez finalizada la ejecución.
   3. En base a la informacion extraida, se enviara un correo al recibidor con la sigueinte informacion:
      - Destinatario : `Pestaña "RECIBIDORES EMAILS", Campo "LISTA EMAILS" (Segun Nombrense Recibidor)`

      - Copia: `Pestaña "RESUMEN CC", Campo "LISTA EMAILS"`
      - Asunto: `Nombre de la carpeta`
      - Cuerpo: `Pestaña "DISTRIBUCION CORREOS", Campo "CUERPO" (Segun Nombrense Recibidor)`
      - Adjunto: `Archivos contenidos en la carpeta`
   4. Generacion de registros de reporteria.

      - Se generara un resumen de la información obtenidoa y para quien se envía:
        - Asunto
        - Destinatario
        - Copia
        - Tipo Caso
        - Cuer
        - Fecha y Hora
      - Se agrupara por cada carpeta.
6. Genera reporte con el resume de la ejecucion.
   1. En caso de que existan carpetas para ejecutar:
      - Genera excel con la reporte resumen de la ejecución.
      - Envia correo con el informe adjunto
        - Desde el Excel de "Configuracion de Envio", pestaña "RECIBIDORES EMAILS", se obtendra los correos de destinatarios.
        - Con archivo de reporte adjunto.
   2. En caso de que no existan carpetas a ejecutar:
      - Envia correo con el informe adjunto
        - Desde el Excel de "Configuracion de Envio", pestaña "RECIBIDORES EMAILS", se obtendra los correos de destinatarios.
        - Se informa que no existieron carpetas a ejecutar.