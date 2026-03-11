from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time

# --- CONFIGURACIÓN DEL NAVEGADOR ---
opciones = Options()
opciones.add_argument('--headless')  # Ejecuta Chrome de fondo, sin abrir la ventana visual
opciones.add_argument('--disable-gpu')
opciones.add_argument('--log-level=3')  # Oculta mensajes molestos de la consola

print("Iniciando el navegador fantasma...")
driver = webdriver.Chrome(options=opciones)

todos_los_partidos = []

# Iteramos las 8 jornadas
for jornada in range(8):
    url = f"https://minifootballleagues.com/tournaments/96?tab=calendar&stage=0&journey={jornada}"
    print(f"Scrapeando Jornada {jornada + 1}...")

    # Le decimos al navegador que abra la URL
    driver.get(url)

    try:
        # ESPERA INTELIGENTE: Esperamos hasta 10 segundos a que aparezca al menos un partido en pantalla
        # Buscamos que cargue la clase que contiene 'styles_containerMatch'
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'styles_containerMatch')]"))
        )
        # Le damos un segundito extra de margen para que renderice los textos internos
        time.sleep(1)

    except Exception as e:
        print(f"  Aviso: No se encontraron partidos o la jornada {jornada + 1} tardó mucho en cargar.")
        continue  # Si falla, saltamos a la siguiente jornada

    # --- EXTRACCIÓN CON BEAUTIFULSOUP ---
    # Ahora sí, extraemos el HTML final con todo el JavaScript ya ejecutado
    html_renderizado = driver.page_source
    soup = BeautifulSoup(html_renderizado, 'html.parser')

    # Buscamos las filas de los partidos (usando la misma lógica de lambda que antes)
    filas_partidos = soup.find_all('div', class_=lambda c: c and 'styles_containerMatch' in c)

    for fila in filas_partidos:
        try:
            # 1. Extraer nombre del equipo local
            elemento_local = fila.find('p', class_=lambda c: c and 'styles_teamNameLeft' in c)
            equipo_local = elemento_local.text.strip() if elemento_local else "Desconocido"

            # 2. Extraer nombre del equipo visitante
            elemento_visitante = fila.find('p', class_=lambda c: c and 'styles_teamNameRight' in c)
            equipo_visitante = elemento_visitante.text.strip() if elemento_visitante else "Desconocido"

            # 3. Extraer el resultado
            elemento_resultado = fila.find('p', class_=lambda c: c and 'styles_text' in c)
            resultado_texto = elemento_resultado.text.strip() if elemento_resultado else ""

            if '-' in resultado_texto:
                goles = resultado_texto.split('-')
                goles_local = int(goles[0].strip())
                goles_visitante = int(goles[1].strip())

                partido = {
                    "jornada": jornada + 1,
                    "equipo_local": equipo_local.title(),
                    "equipo_visitante": equipo_visitante.title(),
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante
                }

                todos_los_partidos.append(partido)

        except Exception as e:
            print(f"  Error procesando un partido: {e}")

# Cerramos el navegador para liberar memoria
driver.quit()

# --- GUARDAR LOS DATOS ---
with open('resultados_liga.json', 'w', encoding='utf-8') as archivo_json:
    json.dump(todos_los_partidos, archivo_json, ensure_ascii=False, indent=4)

print("\n¡Scraping completado con éxito! Revisa tu archivo 'resultados_liga.json'.")