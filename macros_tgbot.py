import json
from datetime import date
from datetime import datetime

#Hay que tener en cuenta el pan, que siempre viene con el menú
#Por cada 100g de pan blanco
BOLLO_PAN = {
    "kcal": 277.0,
    "proteinas": 7.8,
    "grasas": 1.0,
    "carbohidratos": 58.0
}

def resumen_telegram(fichero_json):
    try:
        with open(fichero_json, 'r', encoding='utf-8') as f:
            info = json.load(f)
    except FileNotFoundError:
        return "No se ha encontrado el archivo con la info. nutricional"
    
    #Queremos que el bot de telegram imprima el menú a diario, por lo que 
    #trabajaremos sólo si el día es el que toca.
    dia_actual = date.today().isoformat()
    fecha_norm = date.today().strftime("%d-%m-%Y")

    mensaje= f"Hoy, *{fecha_norm}*, en los comedores universitarios se servirá:\n"
    hay_datos = False

    for sede, fechas in info.items():
        if dia_actual in fechas:
            hay_datos = True
            mensaje += f"\n _*{sede.upper()}*_"

            #Separamos los menús:
            menus_separados={}
            for p in fechas[dia_actual]:
                tipo_menu = p.get('menu', 'OTRO')
                if tipo_menu  not in menus_separados:
                    menus_separados[tipo_menu] = []
                menus_separados[tipo_menu].append(p)

            #Iteramos por cada menú por separado
            for nombre_menu, lista_platos in menus_separados.items():
                mensaje += f"\n\n👨‍🍳​​{nombre_menu.upper()}👩‍🍳​​"

                total_cal = 0
                total_prot = 0
                total_fat = 0
                total_carb = 0

                for p in lista_platos:
                    nombre = p.get('nombre', 'Plato')
                    n = p.get('nutricion')

                    if n:
                        mensaje += f"\n\n🍴 *{nombre}*"
                        p_kcal = n.get('kcal', 0)
                        mensaje += f"\n-kcal: {p_kcal}"
                        p_prot = n.get('proteinas', 0)
                        mensaje += f"\n-proteinas: {p_prot}g"
                        p_fat = n.get('grasas', 0)
                        mensaje += f"\n-grasas: {p_fat}g"
                        p_carbs = n.get('carbohidratos', 0)
                        mensaje += f"\n-carbohidratos: {p_carbs}g"

                        #Acumulamos para el resumen global del menú del día
                        total_cal += p_kcal
                        total_prot += p_prot
                        total_fat += p_fat
                        total_carb += p_carbs

                    else:
                        mensaje += f"\n\nNo hay información nutricional al respecto (comunicar error)"

                mensaje += f"\n\n{'-'*30}"
                mensaje += f"\nTOTAL MENÚ: {round(total_cal, 1)} kcal 🔥"
                mensaje += f"\nMACROS: Prote: {round(total_prot, 1)}g | Carbs: {round(total_carb, 1)}g | Grasas: {round(total_fat, 1)}g"
                mensaje += f"\n{'-'*30}"
    
    if not hay_datos:
        return f"Hoy no hay menú. A buscar tutoriales de cómo hacer lentejas, campeón/a 😹​😹​😹​"
    
    mensaje += f"\n\n🥖 *Recuerda tu bollo de pan:*"
    mensaje += f"\n-kcal: {BOLLO_PAN['kcal']} | prot: {BOLLO_PAN['proteinas']}g | grasas: {BOLLO_PAN['grasas']}g | carbs: {BOLLO_PAN['carbohidratos']}g"
    mensaje += f"\n_NOTA: el total de cada menú ha sido calculado sin tener en cuenta el bollo de pan_"
    mensaje += f"\n\n💧 ¡Y no olvides beber mucha agua! O vino (para los valientes)"

    return mensaje

if __name__ == "__main__":
    print(resumen_telegram("info_nutricional_menu.json"))