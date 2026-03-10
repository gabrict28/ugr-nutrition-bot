import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Configuramos el cliente
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def analizar_con_ia(nombre_plato):
    prompt = f"Analiza nutricionalmente una ración de comedor de: {nombre_plato}"
    
    # Configuramos la respuesta para que sea OBLIGATORIAMENTE un JSON
    config = types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema={
            'type': 'OBJECT',
            'properties': {
                'calorias': {'type': 'INTEGER'},
                'proteinas': {'type': 'NUMBER'},
                'grasas': {'type': 'NUMBER'},
                'carbohidratos': {'type': 'NUMBER'},
            },
            'required': ['calorias', 'proteinas', 'grasas', 'carbohidratos']
        }
    )

    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
            config=config
        )
        
        # La respuesta ya viene como un diccionario de Python gracias al SDK
        return response.parsed
    except Exception as e:
        print(f"❌ Error con Gemini en {nombre_plato}: {e}")
        return None