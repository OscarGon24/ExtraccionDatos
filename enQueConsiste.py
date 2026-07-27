import csv
import time
import pandas as pd
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

def enQueConsiste(link, titulacionColumna):

    driver.get(link)
    time.sleep(1)

    try:

        #Obtiene titulo
        titulacion = driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/h1").text
        print(titulacion)

        #Obtiene subtitulos
        elementosH3 = driver.find_elements(By.XPATH, "//h3")

        for h3 in elementosH3:

            #Obtiene subtitulo del ciclo
            titulo = h3.get_attribute("textContent").strip().replace("\n","")
            
            try:
                H3p = h3.find_element(By.XPATH, "following-sibling::p[1]")
                texto = H3p.get_attribute("textContent").strip().replace("\n","")

                #H3ol = 

                #Para la pagina de Examen general
                if  len(texto) <= 100:#//*[@id="consiste"]/div[2]/div/ol
                    H3ol = driver.find_elements(By.XPATH, "//*[@id='consiste']//ol/li")
                    print(len(H3ol))

                    for ol in H3ol:
                        li = ol.get_attribute("textContent").strip().replace("\n","")
                        texto = texto + li

            except Exception:
                texto = "No tiene párrafo asociado"
                
            print(f"Título: {titulo}")
            print(f"Párrafo: {texto}")
            print("-" * 30)

    except Exception as e:
        print(f"Error durante el proceso: {e}")

try:

    df = pd.read_csv("titulacion_fca.csv")
    listaLinks = df["Link"].tolist()[6:]
    listaTitulacion = df["Titulación"].tolist()[6:]

    for link, titulacion in zip(listaLinks,listaTitulacion):
        if "#consiste" in link:
            enQueConsiste(link, titulacion)

except Exception as e:
    print(f"Error durante el proceso: {e}")

finally:
    driver.quit()