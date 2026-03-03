# 🥗 UGR Nutrition Scraper & Analyzer

Este proyecto automatiza la obtención y el análisis nutricional de los menús de los Comedores Universitarios de la Universidad de Granada (UGR).

## 🚀 Características
- **SCRAPER MULTISEDE**: Obtiene el menú de todas las sedes de los comedores universitarios (Fuentenueva/Cartuja/Aynadamar y PTS).
- **Análisis Nutricional Inteligente**: Conexión con la API de Edamam para obtener kcal, proteínas, grasas e hidratos (en un aproximado del plato como conjunto).
- **Inyector de Estado**: Ajuste automático de valores para alimentos que cambian de peso al cocinarse (arroz, pasta, legumbres...).
- **Caché Local**: Evita peticiones innecesarias a la API, respetando los límites de uso.
- **Sistema de Excepciones**: Diccionario personalizado para platos locales complejos (Fogonero, Ensaladilla Rusa, etc.).

## 🛠️ Instalación
1. Clona el repositorio.
2. Crea un entorno virtual: `python -m venv venv`.
3. Activa el entorno e instala las dependencias:
   ```bash
   pip install -r requirements.txt
   
## PRÓXIMAMENTE:
Estoy trabajando en un bot de telegram que informe cada día sobre el menú que toque junto con su información nutricional.
