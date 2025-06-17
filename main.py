# Punto de entrada de la app (controlador general)

from percepcion.clasificador_intencion import ClasificadorIntencion
from percepcion.procesador_archivos import ProcesadorArchivos
from razonamiento.generar_salidas import Respuestas

def procesar_interaccion(mensaje_usuario: str) -> dict:
# def procesar_interaccion(mensaje_usuario: str, ruta_archivo: str) -> dict:
    
    clasificador = ClasificadorIntencion()
    # procesador = ProcesadorArchivos()

    intencion = clasificador.clasificar(mensaje_usuario)
    # texto = procesador.procesar_archivo(ruta_archivo)

    respuesta = Respuestas(intencion)

    resumen = respuesta.respuesta()


    return {
        "intencion": intencion["intencion"],
        "Respuesta": resumen
        # "texto": texto 
    }

