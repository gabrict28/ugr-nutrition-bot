"""
Proyecto: Bot informativo del aporte nutricional de los menús del SCU.
GABRIEL COBO TRAVÉ - 2026 
Script: analizador_nutricional.py
Preguntamos a Google Gemini por el reporte nutricional de cada plato del menú
"""

import os
import json
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

INPUT_MENU = "menu_ugr.json"
OUTPUT_NUTRI = "info_nutricional_menu.json"
CACHE = "nutricion_cache.json"

#Configuramos el cliente Gemini
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def analisis_ia(nom_plato):
    
    #Generamos el prompt con el que le preguntaremos a la IA
    prompt = f"""
    Actúa como un nutricionista experto en gastronomía española. 
    Analiza una ración estándar del Servicio de Comedores de la Universidad de Granada (España) para el plato: {nom_plato}.
    Ten en cuenta si el alimento se sirve cocinado (arroz, pasta, legumbres, patata) y contrasta la información que encuentres
    para dar la mejor aproximación de la información nutricional.
    Devuelve estrictamente un objeto JSON con estas claves: 
    "kcal" (int), "proteinas" (float), "grasas" (float), "carbohidratos" (float).
    """
    #Configuramos la respuesta para que case con nuestro JSON
    config = types.GenerateContentConfig(
        response_mime_type='application/json',
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', #si en un futuro fuera necesario, podemos definirlo como pro
            contents=prompt,
            config=config
        )
        return json.loads(response.text) #Convertimos el texto a diccionario
    except Exception as e:
        print(f"❌ Error con Gemini en {nom_plato}: {e}")
        return None

#Cargamos el menú
with open(INPUT_MENU, 'r', encoding='utf-8') as input_f:
    datos_menu = json.load(input_f)

#Cargamos la caché
cache = {}
if  os.path.exists(CACHE):
        with open(CACHE, 'r', encoding='utf-8') as cache_f:
            cache = json.load(cache_f)

for sede, dias in datos_menu.items():
    for fecha, platos in dias.items():
        for plato in platos:
            nombre = plato['nombre']

            #Comprobamos si ese plato ya ha sido analizado y se encuentra en la caché
            if nombre in cache:
                plato['nutricion'] = cache[nombre]
            else:
                #Si no está en caché, le preguntamos al sabio
                info = analisis_ia(nombre)
                if info:
                    plato['nutricion'] = info
                    cache[nombre] = info
                    time.sleep(4.5) #La cuota de Gemini Flash es de 15 solicitudes por minuto
                else:
                    print("❌No ha podido ser analizado❌")  

#Guardamos los resultados en el JSON correspondiente
with open(OUTPUT_NUTRI, 'w', encoding='utf-8') as nutrifacts:
    json.dump(datos_menu, nutrifacts, ensure_ascii=False, indent=4)

#Actualizamos la caché
with open(CACHE, 'w', encoding='utf-8') as cache_actualizada:
    json.dump(cache, cache_actualizada, ensure_ascii=False, indent=4)
