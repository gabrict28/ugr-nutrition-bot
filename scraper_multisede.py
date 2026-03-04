"""
Proyecto: Bot informativo del aporte nutricional de los menús del SCU.
GABRIEL COBO TRAVÉ - 2026 
Script: scraper_multisede.py
Scrapping de la web de los SCU para obtener el menú semanal en un json
con formato:
{}
  "Sede (ej: Fuentenueva...)": {
     "Fecha (ej: 01-04-2026)": [
      {
        "nombre": "Arroz con bogavante",
        "nutricion": { "kcal": 130.0, "proteinas": 2.7, ... }
      },
      {
        "nombre": "Mortadela con llaves",
        "nutricion": { ... }
      }
    ]
  },
  "Sede (ej: PTS)": { ... }
}
"""

import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

#Función para convertir las fechas de la web "MARTES, 1 DE ABRIL  DE  2026"
#a formato útil "01-04-2026"
def normalizar_fecha_scu(fecha_bruto):
    meses = {
        "ENERO": 1, "FEBRERO": 2, "MARZO": 3, "ABRIL": 4, "MAYO": 5, "JUNIO": 6,
        "JULIO": 7, "AGOSTO": 8, "SEPTIEMBRE": 9, "OCTUBRE": 10, "NOVIEMBRE": 11, "DICIEMBRE": 12
    }

    try:
        partes=fecha_bruto.upper().split()

        if len(partes) < 6:
            return None
        
        d = int(partes[1])
        m = meses[partes[3]]
        y = int(partes[5])

        fecha = datetime(y,m,d)

        return fecha.strftime("%Y-%m-%d")
    except Exception as e:
        return None

#Vamos a organizar en sedes (Fuentenueva/Cartuja/Aynadamar o PTS) y en semanas
url = "https://scu.ugr.es/"



try:
    respuesta = requests.get(url)
    soup = BeautifulSoup(respuesta.text, 'html.parser')

    #Establecemos la separación por sede:
    info_completa = {
        "Fuentenueva/Cartuja/Aynadamar": {},
        "PTS": {}
    }

    sede_actual = "Fuentenueva/Cartuja/Aynadamar"

    #En el HTML la distinción entre sedes viene especificada entre <h1> </h1>
    elementos = soup.find_all(['h1','table'])

    for e in elementos:
        #Titular h1: estaremos hablando de una sede
        if e.name == 'h1':
            titulo_h1 = e.get_text().lower() #minúsculas para trabajar con uniformidad
            if "fuentenueva" in titulo_h1:
                sede_actual = "Fuentenueva/Cartuja/Aynadamar"
            elif "pts" in titulo_h1:
                sede_actual = "PTS"
            continue #habremos acabado con el titulo
        
        #Tabla de menú: uso la lógica del scraper para un solo dia ("test_scraper.py") pero 
        #adaptándola al uso de los elementos para no recurrir al soup.find que no funcionaría
        if (e.name == 'table') and ('inline' in e.get('class',[])):
            
            fecha_actual = None
            menu_dia = []
            seccion = "Menú estándar"

            #Recorremos las filas HTML teniendo en cuenta que la fila de plato está compuesta como sigue:
            # td[0]: categoría (Primero/Segundo/Postre)
            # td[1]: nombre del plato con <strong>
            # td[2]: los alérgenos dentro de un enlace <a>
            print(f"\n")
            for fila in e.find_all('tr'):
                
                #Si es un encabezado de fecha, la gestionamos
                th_fecha = fila.find('th')
                if th_fecha:
                    fecha_norm = normalizar_fecha_scu(th_fecha.get_text(strip=True))
                    #Guardamos los platos acumulados de un día anterior
                    if fecha_actual and menu_dia:
                        info_completa[sede_actual][fecha_actual] = menu_dia

                    #Actualizamos la fecha y reseteamos el menú
                    fecha_actual = fecha_norm
                    menu_dia = []
                    seccion = "Menú estándar"
                    continue
                
                #Si es un cambio de sección:
                celdas = fila.find_all('td')
                if len(celdas) >= 2: 
                    texto_celda_0 = celdas[0].text.strip()
                    #Si es una fila que indica el tipo de menú
                    if "Menú" in texto_celda_0:
                        if "2" in texto_celda_0:
                            seccion = "Menú ovolactovegetariano"
                        else:
                            seccion = "Menú estándar"
                        continue #No necesitamos procesar nada más en esta fila
                
                    #Si es una fila de plato:
                    nombre_bruto = celdas[1].find('strong')

                    #Verifico que que texto_celda_1 no sea vacío para que no añada "Consultar ingredientes semanales"
                    if nombre_bruto and texto_celda_0: 
                        nombre_plato = nombre_bruto.text.strip()
                        #hay platos sin descripción de alérgenos (véanse algunos postres)
                        #pero la tabla HTML es consistente y aunque la celda esté vacía
                        #esta existe de la forma <td> </td>
                        alergenos = ""
                        if len(celdas) > 2: 
                            alergenos = celdas[2].text.strip().replace("\n", " ")
                            
                        descripcion_plato = {
                            "menu": seccion,
                            "categoria": texto_celda_0,
                            "nombre": nombre_plato,
                            "alergenos": alergenos
                        }
                        menu_dia.append(descripcion_plato)
            if menu_dia:
                info_completa[sede_actual][fecha_actual] = menu_dia

except Exception as e:
    print(f"Se jodio el asunto {e}")

nom_archivo = "menu_ugr.json"
#Abrimos el archivo en modo escritura y con utf-8 para las tildes y la ñ
with open(nom_archivo, 'w', encoding='utf-8') as archivo:
    #Volcamos el menu en el archivo json 
    json.dump(info_completa, archivo, ensure_ascii=False, indent=4)