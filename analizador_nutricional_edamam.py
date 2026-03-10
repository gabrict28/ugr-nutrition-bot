"""
Proyecto: Bot informativo del aporte nutricional de los menús del SCU.
GABRIEL COBO TRAVÉ - 2026 
Script: analizador_nutricional_edamam.py
Peticiones a la API para el reporte nutricional de cada plato del menú

Es importante notar que los de la API son un pelín sionistas y la única manera de poder
usarla sin pagar es mediante un plan que permite sólo 5 consultas por minuto, luego obligaremos
al programa a esperar 12 segundos entre consulta y consulta (60/5=12).

NOTA: este archivo pertenece a la primera versión del bot, ahora se usa el "analizador_nutricional.py" para las
estimaciones ya que Edamam daba unos estimados malísimos siendo generosos.
"""


import json
import requests
import time
import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator #la API trabaja en inglés

load_dotenv()
APP_ID = os.getenv("BD_APP_ID")
APP_KEY = os.getenv("BD_APP_KEY")
INPUT_MENU = "menu_ugr.json"
OUTPUT_NUTRI = "info_nutricional_menu.json"
CACHE = "nutricion_cache.json"
EXCEPCIONES = "excepciones.json"

#Cargamos el diccionario de las excepciones
excepciones = {}
if os.path.exists(EXCEPCIONES):
    with open(EXCEPCIONES, 'r', encoding='utf-8') as diccionario_excepciones:
        excepciones = json.load(diccionario_excepciones)

def analisis_api(plato_bruto):
    #Limpiamos el nombre para asegurarnos de que la api lo entienda
    plato_es = plato_bruto.split('(')[0].strip().lower()
    
    #Traducimos el plato al inglés para pasárselo a la API
    if plato_es in excepciones:
        plato_en = excepciones[plato_es]
    else:
        try: 
            plato_en = GoogleTranslator(source='es', target='en').translate(plato_es).lower()
        except: 
            plato_en = plato_es #por si falla la traducción

    #Inyector de estado ya que hay comidas que cambian su valor nutricional (proporcionalmente) 
    #al cocinarse
    alimentos_secos = ["rice", "macaroni", "pasta", "spaghetti", "lentils",
                       "beans", "chickpeas", "potato", "potatoes"]
    
    for ingr in alimentos_secos:
        #Si encontramos alguno de estos alimentos en el plato, tenemos que indicarle a la API
        #que son cocinados (no es lo mismo 100g de arroz en seco que hervido)
        if (ingr in plato_en) and (f"cooked {ingr}" not in plato_en) and (f"boiled {ingr}" not in plato_en):
            plato_en = plato_en.replace(ingr, f"cooked {ingr}")

    #NOTA: a partir de aquí seguimos un plan un poco extraño ya que la API es caprichosa.
    #Hay platos cuyo nombre en español es compuesto; p.ej: "Fogonero Mare Nostrum" y su
    #traducción no se encuentra en la BD, por lo que en caso de que un plato falle, reducimos
    #su nombre a lo esencial, si seguimos el ejemplo de antes quedaría "Fogonero" y preguntaríamos
    #a la BD simplemente por la información nutricional de este pescado.
    #NOTA 2: esta """mejora""" es una mierda y la he comentado por si luego me arrepiento

    #Función interna para optimizar código
    def llamarBD(nombre):
        url = "https://api.edamam.com/api/food-database/v2/parser"
        params = {
            'app_id': APP_ID,
            'app_key': APP_KEY,
            'ingr': nombre,
            'nutrition-type': 'cooking' #los valores cambian en la BD si el alimento está cocinado
        }
        r = requests.get(url, params=params)
        if r.status_code == 200:
            data = r.json()
            
            #Al ser la mayoría platos compuestos, en hints la API buscará la información nutricional
            #en su base de datos de alimentos ya existentes.
            if 'hints' in data and data['hints']:
                return data['hints'][0]['food']['nutrients']
            #Al parsear la API analiza los ingredientes y si se ve sobrepasada a veces descarta
            #algún ingrediente en platos compuestos (por eso es la segunda opción)
            elif 'parsed' in data and data['parsed']:
                return data['parsed'][0]['food']['nutrients']
        return None
    
    #Intentamos con el nombre completo
    print(f"Nom INGLES: {plato_en}")
    nutrientes = llamarBD(plato_en)

    #Si falla, reducimos al ingrediente esencial y lo volvemos a intentar
    if not nutrientes:# and len(plato_en.split())>1:
        #ingr_ppal_en = plato_en.split()[-1] #En inglés el sujeto suele ir al final
        #nutrientes = llamarBD(ingr_ppal_en)
        print(f"mecagoendiez")
    
    if nutrientes:
        return{
            "kcal": round(nutrientes.get('ENERC_KCAL',0),1),
            "proteinas": round(nutrientes.get('PROCNT',0),1),
            "grasas": round(nutrientes.get('FAT',0),1),
            "carbohidratos": round(nutrientes.get('CHOCDF',0),1)
        }
    return None

with open(INPUT_MENU, 'r', encoding='utf-8') as input_f:
    datos_menu = json.load(input_f)

#Esto es para ahorrar trabajo ya que tenemos consultas reducidas a la BD
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
                info = analisis_api(nombre)

                if info:
                    plato['nutricion'] = info
                    cache[nombre] = info
                    time.sleep(2)
                else:
                    print("❌No ha podido ser analizado❌")    

#Guardamos los datos en el json
with open(OUTPUT_NUTRI, 'w', encoding='utf-8') as nutrifacts:
    json.dump(datos_menu, nutrifacts, ensure_ascii=False, indent=4)

#Guardamos la caché
with open(CACHE, 'w', encoding='utf-8') as cache_actualizada:
    json.dump(cache, cache_actualizada, ensure_ascii=False, indent=4)