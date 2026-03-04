"""
Proyecto: Bot informativo del aporte nutricional de los menús del SCU.
GABRIEL COBO TRAVÉ - 2026 
Script: calculadora_macros_menu.py
Base del "macros_tgbot.py"
"""

import json

INPUT_NUTRI_MENU="info_nutricional_menu.json"

def calcular_macros():
    #Abrimos el JSON que contiene los menús con su correspondiente información
    #nutricional 
    with open(INPUT_NUTRI_MENU, 'r', encoding='utf-8') as menu:
        info = json.load(menu)

        for sede, dias in info.items():
            print(f"SEDE: {sede.upper()}")
            
            for fecha, platos in dias.items():
                print(f"{fecha}")
                
                #Separamos los menús:
                menus_separados={}
                for p in platos:
                    tipo_menu = p.get('menu', 'OTRO')
                    if tipo_menu  not in menus_separados:
                        menus_separados[tipo_menu] = []
                    menus_separados[tipo_menu].append(p)

                #Iteramos por cada menú por separado
                for nombre_menu, lista_platos in menus_separados.items():
                    print(f"🍴{nombre_menu.upper()}🍴")

                    total_cal = 0
                    total_prot = 0
                    total_fat = 0
                    total_carb = 0

                    #Imprimimos cada plato con su información nutricional
                    for p in lista_platos:
                        nombre = p.get('nombre', 'Plato')
                        nutri = p.get('nutricion')

                        if nutri:
                            p_kcal = nutri.get('kcal', 0)
                            p_prot = nutri.get('proteinas', 0)
                            p_fat = nutri.get('grasas', 0)
                            p_carbs = nutri.get('carbohidratos', 0)
                            print(f" {nombre[:30]:<30} | {p_kcal:>5} kcal | P: {p_prot:>4}g | CH: {p_carbs:>4}g | G: {p_fat:>4}g")

                            #Acumulamos para el resumen global del menú del día
                            total_cal += p_kcal
                            total_prot += p_prot
                            total_fat += p_fat
                            total_carb += p_carbs
                        else:
                            print(f"No hay información nutricional al respecto (comunicar error)")
                
                    #Resumen por menú
                    print(f"{'-'*40}")
                    print(f"TOTAL MENÚ: {round(total_cal, 1)} kcal")
                    print(f"MACROS: Prot: {round(total_prot, 1)}g | Carbs: {round(total_carb, 1)}g | Grasas: {round(total_fat, 1)}g")
                    print(f"{'-'*40}")

if __name__ == "__main__":
    calcular_macros()