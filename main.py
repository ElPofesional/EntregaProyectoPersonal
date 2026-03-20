import agentConfig
from dotenv import load_dotenv
from agents import Agent, Runner, trace, WebSearchTool
from rich.console import Console
from rich.markdown import Markdown
import asyncio

# TODO: "Posible mejora: modo "Watson", que en vez de dar la respuesta directamente, guíe al usuario para que llegue a la respuesta por sí mismo."

load_dotenv(override=True)

console = Console()#Para que al imprimir la respuesta esta tenga la estética intencionada.


async def profesor(mensaje: str, historial: list, ventana: int = 5):

    # Configuración del agente.
    agente = Agent(#Se configura en agenteConfig.py
        name=agentConfig.nombre,
        instructions=agentConfig.instrucciones,
        model=agentConfig.modelo,
        tools=[WebSearchTool()]#Acceso a la red. Esto aumenta el tiempo de ejecución y el precio.
    )
    
    # Preparación del historial - Gradio pasa el historial en forma de  lista de diccionarios, y la IA lo necesita en string.
    parejas_de_mensajes = []#Una pareja de mensajes es una pregunta y su respuesta.
    posicion = 0
    while posicion < len(historial) - 1:
        entrada_actual = historial[posicion]
        salida_actual = historial[posicion + 1] if posicion + 1 < len(historial) else None

        # Extraer texto del mensaje actual
        content = entrada_actual.get('content', [])#Usar .get evita errores si content no existe, aunque ya lo comprueba el if.
        usuario_text = content[0].get('text', '') if isinstance(content[0], dict) else ''
        
        # Extraer texto del siguiente mensaje
        content = salida_actual.get('content', [])
        asistente_text = content[0].get('text', '') if isinstance(content[0], dict) else ''

        #Se almacena la pareja de mensajes.
        parejas_de_mensajes.append((usuario_text, asistente_text))
        posicion += 2  # Saltamos dos para llegar al siguiente par


    # Se corta el historial para adaptarlo a la ventana de contexto seleccionada.
    historial_cortado = parejas_de_mensajes[-ventana:] if len(parejas_de_mensajes) > ventana else parejas_de_mensajes
    
    # Formatear el historial cortado como un string legible para el agente
    historial_en_texto = ""
    for mensajeUsuario, respuestaIA in historial_cortado:
        historial_en_texto += f"Usuario: {mensajeUsuario}\nProfesor: {respuestaIA}\n\n"
    
    # Crear el mensaje completo con historial + mensaje actual
    mensaje_completo = historial_en_texto + f"Pregunta actual: {mensaje}\nTu respuesta:"
    
    # Ejecutar el agente con el mensaje completo (incluyendo memoria limitada)
    with trace(workflow_name="Profesor"):
        respuesta = await Runner.run(agente, mensaje_completo)
    
    console.print(Markdown(respuesta.final_output))
    return respuesta.final_output


def main():
    # Evitar fallos cuando no hay stdin (por ejemplo, en contenedores de docker sin posibilidad de interactuar con el código)
    import sys

    if not sys.stdin.isatty():
        console.print("[red]No se puede leer desde stdin (no hay tty). Ejecuta `python app.py` o usa `docker run -it ...`.[/red]")
        sys.exit(1)

    try:
        prompt = input("Escribe tu mensaje: ")
    except EOFError:
        console.print("[red]EOFError: stdin cerrado. Ejecuta el script en un terminal interactivo.[/red]")
        sys.exit(1)

    asyncio.run(profesor(prompt, []))


if __name__ == "__main__":
    main()
