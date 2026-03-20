# Profesor IA

Este proyecto es una aplicación de chat sencilla que ejecuta un agente ("Profesor") que responde a las preguntas con explicaciones y ejemplos.


## Requisitos previos

1. Una **API Key de OpenAI** con saldo. 
2. Un navegador, la aplicación de docker abierta y activa, y una terminal.


---

## Configuración (API Key)
Introduce tu API Key (directamente del portapapeles para evitar errores) en el `.env`, donde pone `OPENAI_API_KEY=`.




## Ejecutar con Docker

1) Construir la imagen:

```bash
docker build -t mi-proyecto-uv:latest .
```

2) Ejecutar el contenedor:

```bash
docker run --rm -p 7860:7860 mi-proyecto-uv:latest
```

En cuant aparezca algo similar a `Installed 216 packages in 8.47s` visita http://0.0.0.0:7860/ en tu navegador. Para apagar el servidor entra en la terminal y pulsa `Ctrl+C`

---

## Modificar el comportamiento del "Profesor" para customizar el agente

**`agentConfig.py`** controla el nombre del agente, instrucciones y el modelo.
