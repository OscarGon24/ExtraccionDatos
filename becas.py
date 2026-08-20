import csv
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

opciones = Options()
opciones.add_argument('--ignore-certificate-errors')
opciones.add_argument('--ignore-ssl-errors')
opciones.set_capability('acceptInsecureCerts', True)

prefs = {"https_only_mode_enabled": False}
opciones.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=opciones)

try:
    url = "https://www.fca.unam.mx/estudiante/becas.php"
    driver.get(url)
    time.sleep(1)

    contenido = []

    pestanas = driver.find_elements(By.XPATH, "//*[@id='becasTabs']/*")
    print(len(pestanas))

    #//*[@id="video"]
    body = driver.find_element(By.XPATH, "//*[@id='video']")
    body = body.get_attribute("textContent").strip().replace("\n", "")
    body = " ".join(body.split())

    titulo = body[:45]
    body = body[46:]
    contenido.append([titulo, body])

    #//*[@id="becaAlimenticia"]
    #//*[@id="becaAlimenticia"]/div/h4
    body = driver.find_element(By.XPATH, "//*[@id='becaAlimenticia']")
    titulo = body.find_element(By.TAG_NAME, "h4")
    titulo = titulo.get_attribute("textContent").strip().replace("\n", "")
    enlaces = body.find_elements(By.TAG_NAME, "a")

    print(len(enlaces))

    links = []

    for enlace in enlaces:

        texto = enlace.get_attribute("textContent").replace("\n", "").strip()
        link = enlace.get_attribute("href")

        links.append(f"{texto}: {link}")

    body = " | ".join(links)
    contenido.append([titulo, body])

    #becas

    for n in range(9):

        body = driver.find_element(By.XPATH, f"//*[@id='beca{n+1}']")
        body = body.get_attribute("textContent").strip().replace("\n", "")
        body = " ".join(body.split())

        if n == 0:
            t = 20
        elif n == 1:
            t = 32
        elif n == 2 or n == 9:
            t = 44
        elif n == 3 or n == 4:
            t = 29
        elif n == 5:
            t = 56
        elif n == 6:
            t = 57
        elif n == 7:
            t = 48
        elif n == 8:
            t = 51
        
        titulo = body[:t]
        body = body[t+1:]
        contenido.append([titulo, body])

    archivo_csv = "becas_fca.csv"
    cabeceras = ["Tema","Información"]

    with open(archivo_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(cabeceras)
        writer.writerows(contenido)
        
    print(f"¡Éxito! Datos guardados correctamente en '{archivo_csv}'")

except Exception as e:
    print(f"Error de exception: {e}")
finally:
    driver.quit()