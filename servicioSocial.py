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
opciones.page_load_strategy = 'eager'

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

    time.sleep(2)

    #GENERALIDADES
    print("Generalidaes")
    for t in range(len(tabs)):
        if t == 0:
            tema = general.find_element(By.XPATH, f"./div/h4")
            tema = tema.get_attribute("textContent").strip().replace("\n", " ").lower()
            p = general.find_element(By.XPATH, f"./div/p")
            p = p.get_attribute("textContent").strip().replace("\n", " ").lower()
            contenido.append(["Generalidades", tema, p])

        else:
            tema = general.find_element(By.XPATH, f"./div/h5[{t}]")
            tema = tema.get_attribute("textContent").strip().replace("\n", " ").lower()
            p = general.find_element(By.XPATH, f"./div/p[{t}+1]")
            p = p.get_attribute("textContent").strip().replace("\n", " ").lower()
            contenido.append(["Generalidades", tema, p])

    #REGISTRO
    print("Registro")
    tema = registro.find_element(By.XPATH, f"./div/h4")
    tema = tema.get_attribute("textContent").strip().replace("\n", " ").lower()
    p = registro.find_element(By.XPATH, f"./div/p")
    p = p.get_attribute("textContent").strip().replace("\n", " ").lower()
    ul = registro.find_elements(By.XPATH, f"./div/div//a")

    btn = Wait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='servicioSocialTabs']/li[2]/button"))
    )
    btn.click()

    for a in ul:
        a.click()

        modal = Wait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "modalContenido"))
        )
        time.sleep(2)

        try:
            titulo_elemento = modal.find_element(By.XPATH, ".//header/h4 | .//div[1]/h4 | .//h4 | .//h5")
            titulo = titulo_elemento.get_attribute("textContent").strip().replace("\n", " ")
            print(f"Título extraído: {titulo}")
        except:
            titulo = "Título no identificado"
            print("Advertencia: Este modal tiene un HTML distinto, no se halló el título.")

        body_element = modal.find_element(By.XPATH, ".//div[contains(@class, 'modal-body')] | .//div[1]/div")
        
        body_texto = body_element.get_attribute("textContent")
        body_limpio = " ".join(body_texto.split())

        enlaces_modal = body_element.find_elements(By.TAG_NAME, "a")
        links_extraidos = []

        for enlace in enlaces_modal:
            texto_link = " ".join(enlace.get_attribute("textContent").split())
            url = enlace.get_attribute("href")
            
            if url:
                links_extraidos.append(f"{texto_link}: {url}")

        if links_extraidos:
            body_final = f"{body_limpio} | Enlaces de apoyo: " + " | ".join(links_extraidos)
        else:
            body_final = body_limpio

        contenido.append([tema, titulo, body_final])

        boton_cerrar = driver.find_element(By.XPATH, "//div[@id='contenidoModal']//button[contains(@class, 'btn-close')]")
        boton_cerrar.click()

        Wait(driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "modalContenido"))
        )
        time.sleep(0.5)

    time.sleep(3)
    btn = Wait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='servicioSocialTabs']/li[3]/button"))
    )
    btn.click()
    time.sleep(1)


    #TERMINO
    print("Término")
    seccion = "Término"

    termino = driver.find_element(By.XPATH, "//*[@id='termino']/div")
    elementos = termino.find_elements(By.TAG_NAME, "a")
    print(len(elementos))

    for elemento in elementos:
        time.sleep(2)
        titulo = elemento.get_attribute("textContent").strip().replace("\n", " ")
        enlace = elemento.get_attribute("href").strip()
        print(titulo)
        print(enlace)

        if "php" in enlace:
            elemento.click()
            time.sleep(2)

            #//*[@id="modalContenido"]/section/div/div/div[2]
            modal = driver.find_element(By.XPATH, "//*[@id='modalContenido']/section/div/div/div[2]")

            h5 = modal.find_element(By.TAG_NAME, "h5")
            h5 = h5.get_attribute("textContent").replace("\n", "").strip()

            try:
                body = modal.find_element(By.XPATH, ".//div/div[1]")
                body = body.get_attribute("textContent").replace("\n", "").strip()
            except Exception as e:
                body = ""
            
            enlaces = modal.find_elements(By.TAG_NAME, "a")

            links = []

            for enlace in enlaces:
                texto = enlace.get_attribute("textContent").lower().strip()
                link = enlace.get_attribute("href")

                textoLink = texto + ": " + link
                links.append(textoLink)
            print(links)
            
            body_limpio = " ".join(body.split())
            body = f"{h5} {body_limpio} | Enlaces: " + " | ".join(links)
            
            contenido.append([seccion, titulo, body])

            boton_cerrar = driver.find_element(By.XPATH, "//div[@id='contenidoModal']//button[contains(@class, 'btn-close')]")
            boton_cerrar.click()

            Wait(driver, 10).until(
                EC.invisibility_of_element_located((By.ID, "modalContenido"))
            )
            time.sleep(0.5)
        else:
            contenido.append([seccion, titulo, enlace])

    time.sleep(2)
    btn = Wait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='servicioSocialTabs']/li[3]/button"))
    )
    btn.click()
    time.sleep(1)

    #Liberación
    print("Liberación")
    seccion = "Liberación"
    enlace = driver.find_element(By.XPATH, "//*[@id='liberacion']/div/a")
    texto = enlace.get_attribute("textContent").strip()
    enlace = enlace.get_attribute("href")

    contenido.append([seccion, texto, enlace])

    time.sleep(2)
    btn = Wait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='servicioSocialTabs']/li[4]/button"))
    )
    btn.click()
    time.sleep(1)

    #Baja
    print("Baja")
    seccion = "Baja"
    enlace = driver.find_element(By.XPATH, "//*[@id='baja']/div/a")
    texto = enlace.get_attribute("textContent").strip()
    enlace = enlace.get_attribute("href")

    contenido.append([seccion, texto, enlace])

    time.sleep(2)
    btn = Wait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='servicioSocialTabs']/li[5]/button"))
    )
    btn.click()
    time.sleep(1)

    #Reglamento
    print("Reglamento")
    seccion = "Reglamento"
    enlace = driver.find_element(By.XPATH, "//*[@id='reglamento']/div/a")
    texto = enlace.get_attribute("textContent").strip()
    enlace = enlace.get_attribute("href")

    contenido.append([seccion, texto, enlace])

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