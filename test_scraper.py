"""
Proyecto: Bot informativo del aporte nutricional de los menús del SCU.
GABRIEL COBO TRAVÉ - 2026 
Script: identificador.py
Pruebas iniciales del scrapping
"""

import json
import requests
from bs4 import BeautifulSoup

# soup.find("etiqueta", id="valor") --> Busca el primer elemento que coincida
# soup.find_all("etiqueta", class_="valor") --> Busca todos los elementos que coincidan
url = "https://scu.ugr.es/"

try:
    #Petición HTTP GET  a la web de los comedores
    respuesta = requests.get(url) 
    #Traducimos el contenido HTML para que python lo pueda leer (lo parseamos)
    soup = BeautifulSoup(respuesta.text, 'html.parser') 
    #Prueba tonta
    #print(f"Conexión establecida, conectados a {soup.title.string}")

    #Prueba tonta enlaces
    #enlaces = soup.find_all("a") #para buscar todos los enlaces de la página
    #print(f"Enlaces encontrados: {len(enlaces)}")
    #for enlace in enlaces[:5]: #imprime los primeros 5 enlaces
        #print(f"- Texto: {enlace.text.strip()} | URL: {enlace.get('href')}")

    #Sabemos que la fecha está dentro de una etiqueta <th> "table header", la buscamos
    #para imprimirla
    #NOTA: tr significa "table row" y define cada fila de la tabla HTML
    #      td significa "table data" y es una celda dentro de la fila

    #Obtenemos la tabla de la clase inline (se puede ver en el HTML de la página)
    tabla_menu = soup.find('table', class_='inline')

    if tabla_menu:
        #Buscamos el primer th que contendrá la fecha
        fecha_limpia = tabla_menu.find('th').text.strip() #text para texto y strip para limpiarlo
        #print(f"---   {fecha_limpia}   ---")
        
        #Lista para los platos del día
        menu_dia = []
        seccion = "Menú estándar"

        #Recorremos las filas HTML teniendo en cuenta que la fila de plato está compuesta como sigue:
        # td[0]: categoría (Primero/Segundo/Postre)
        # td[1]: nombre del plato con <strong>
        # td[2]: los alérgenos dentro de un enlace <a>
        print(f"\n")
        for fila in tabla_menu.find_all('tr'):
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

                #Verifico que que texto_celda_0 no sea vacío para que no añada "Consultar ingredientes semanales"
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
            
        #IMPRESIÓN:
        print(f"🍴 DÍA {fecha_limpia.upper()} 🍴")
        print(f"\n")

        for tipo in ["Menú estándar", "Menú ovolactovegetariano"]:
            print(f"{tipo.upper()}")
            print("-"*20)

            #Filtramos los platos que pertenecen a cada menú
            platos_cada_tipo = [p for p in menu_dia if p['menu'] == tipo]

            for p in platos_cada_tipo:
                categoria = p['categoria'].ljust(4)
                alergenos = ""
                if p['alergenos']:
                    alergenos = f"   ⚠️   Alérgenos: {p['alergenos']}"
                print(f"{categoria} --> {p['nombre']} {alergenos}")
            print("\n")

        print("="*50)
        print(f"Procesados {len(menu_dia)} platos correctamente")
        print("="*50)
        

    else:
        print(f"Error para inline")


except Exception as e:
    print(f"Se jodio el asunto {e}")

nom_archivo = "menu_test.json"
#Abrimos el archivo en modo escritura y con utf-8 para las tildes y la ñ
with open(nom_archivo, 'w', encoding='utf-8') as archivo:
    #Volcamos el menu en el archivo json 
    json.dump(menu_dia, archivo, ensure_ascii=False, indent=4)