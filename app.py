import gradio as gr  # https://www.gradio.app/guides/creating-a-chatbot-fast
from main import profesor
"""
Versión 1: una pregunta y una respuesta. 
interface = gr.Interface(
    fn=profesor,
    inputs=[gr.Textbox(label="Pregunta", lines=2,
                       placeholder="Ejemplo: Háblame de la fotosíntesis")],
    outputs=[gr.Markdown(label="Respuesta del Profesor")],
    title="Profesor",
    theme="compact"
)
interface.launch()
"""

interfaz = gr.ChatInterface(
    fn=profesor,
    additional_inputs=[
        gr.Slider(#Para alterar el tamaño del historial.
            minimum=1,
            maximum=20,
            value=5,
            step=1,
            label="Acceso de la IA al historial de la conversación",
            info="A mayor ventana de contexto, menor eficiencia y mayor costo.\nA mayor ventana de contexto, mayor memoria.")
    ],
    title="Profesor",    description="Un profesor amable y paciente que responde a las preguntas de los estudiantes de manera clara y concisa, proporcionando ejemplos en todo momento.",
)
if __name__ == "__main__":
    import sys
    
    # Silenciar advertencias de Gradio
    import os
    os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
    
    # launch() mantiene el proceso vivo por sí solo
    interfaz.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        debug=False,
        inline=False,
        quiet=False,
        max_threads=40  # Para mejor concurrencia
    )
