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
    driver.get("https://www.fca.unam.mx/estudiante/servicio_social.php")
    time.sleep(1)

    xpath = "/html/body/div[1]"

    tabs = driver.find_elements(By.XPATH, f"{xpath}/ul/*")
    print("Número de pestañas encontradas:", len(tabs))

    contenido = []
    
    general = driver.find_element(By.ID, "general")
    registro = driver.find_element(By.ID, "registro")

    for t in range(len(tabs)):
        if t == 0:
            tema = general.find_element(By.XPATH, f"./div/h4")#//*[@id="general"]/div/h4
            tema = tema.get_attribute("textContent").strip().replace("\n", " ").lower()
            p = general.find_element(By.XPATH, f"./div/p")#//*[@id="general"]/div/p[1]
            p = p.get_attribute("textContent").strip().replace("\n", " ").lower()
            contenido.append(["generalidades", tema, p])

        else:
            tema = general.find_element(By.XPATH, f"./div/h5[{t}]")#//*[@id="general"]/div/h5[1]
            tema = tema.get_attribute("textContent").strip().replace("\n", " ").lower()
            p = general.find_element(By.XPATH, f"./div/p[{t}+1]")#//*[@id="general"]/div/p[2]
            p = p.get_attribute("textContent").strip().replace("\n", " ").lower()
            contenido.append(["generalidades", tema, p])

    tema = registro.find_element(By.XPATH, f"./div/h4")#//*[@id="registro"]/div/h4
    tema = tema.get_attribute("textContent").strip().replace("\n", " ").lower()
    p = registro.find_element(By.XPATH, f"./div/p")#//*[@id="registro"]/div/p
    p = p.get_attribute("textContent").strip().replace("\n", " ").lower()
    ul = registro.find_elements(By.XPATH, f"./div/div//a")#//*[@id="registro"]/div/div

    btn = Wait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='servicioSocialTabs']/li[2]/button"))
    )
    btn.click()

    for a in ul:
        a.click()

        x = Wait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='contenidoModal']/div/div/div[1]/button"))
        )
        x.click()

        #//*[@id="modalContenido"]/section/div/div/header/h4
        modal = driver.find_element(By.ID, "modalContenido")

        titulo = modal.find_element("./section/div/div/header")
        titulo = titulo.get_attribute("h4")
        print(titulo)

        #href = a.get_attribute("href").strip().replace("\n", " ").lower()
        #texto = a.get_attribute("textContent").strip().replace("\n", " ").lower()

        #serv = f"Para el servivio {texto} el link es: {href}"

        #contenido.append([tema, p, serv])



    archivo_csv = "servicioSocial_fca.csv"
    cabeceras = ["Sección", "Tema","Información"]

    with open(archivo_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(cabeceras)
        writer.writerows(contenido)
        
    print(f"¡Éxito! Datos guardados correctamente en '{archivo_csv}'")

except Exception as e:
    print("Error al iniciar sesión:", e)
    driver.quit()
    exit()

finally:
    driver.quit()