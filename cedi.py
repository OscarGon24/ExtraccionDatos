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
    url = "https://idiomas.fca.unam.mx/index.php"
    driver.get(url)
    time.sleep(1)

    contenido = []

    #//*[@id="cta-profesional"]/div/div/div[2]
    elementos = driver.find_elements(By.XPATH, "//*[@id='cta-profesional']/div/div/div[2]/*")

    titulo = ""
    informacion = ""

    for elemento in elementos:
        etiqueta = elemento.tag_name.lower()
    
        if etiqueta == "h2":
            titulo = elemento.get_attribute("textContent").strip().replace("\n","")
            
        elif etiqueta == "p":
            informacion = elemento.get_attribute("textContent").strip().replace("\n","")
            if informacion:
                contenido.append([titulo, informacion])
                
        elif etiqueta == "div":
            try:
                titulo_h6 = elemento.find_element(By.TAG_NAME, "h6")
                titulo = titulo_h6.get_attribute("textContent").strip().replace("\n", "")
                
                info_p = elemento.find_element(By.TAG_NAME, "p")
                informacion = info_p.get_attribute("textContent").strip().replace("\n", "")
                
                if informacion:
                    contenido.append([titulo, informacion])
            except:
                pass
                
    titulo = driver.find_element(By.XPATH, "//*[@id='requisito']/div/div[1]/h1")
    titulo = titulo.get_attribute("textContent").strip().replace("\n","")

    id = "//*[@id='plan2012']"

    subtitulo = driver.find_element(By.XPATH, f"{id}/h2")
    subtitulo = subtitulo.get_attribute("textContent")

    tituloDiv = titulo + " - " + subtitulo
    print(tituloDiv)

    p = driver.find_element(By.XPATH, f"{id}/p")
    p = p.get_attribute("textContent").strip().replace("\n","")

    p_limpio = " ".join(p.split())

    ul = driver.find_elements(By.XPATH, f"{id}/ul/*")

    lis = []

    for li in ul:
        li = li.get_attribute("textContent").strip().replace("\n","")
        li_limpio = " ".join(li.split())

        lis.append(li)

    informacion = p_limpio + " -".join(lis)

    contenido.append([tituloDiv, informacion])

    #PLANES ANTERIORES
    id = "//*[@id='planesAnteriores']"

    btn = Wait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='requisito']/div/div[2]/div[1]/div[2]"))
    )
    
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(1)

    subtitulo = driver.find_element(By.XPATH, f"{id}/h2")
    subtitulo = subtitulo.get_attribute("textContent")

    tituloDiv = titulo + " - " + subtitulo
    print(tituloDiv)

    p = driver.find_element(By.XPATH, f"{id}/p")
    p = p.get_attribute("textContent").strip().replace("\n","")

    p_limpio = " ".join(p.split())

    ul = driver.find_elements(By.XPATH, f"{id}/ul/*")

    lis = []

    for li in ul:
        li = li.get_attribute("textContent").strip().replace("\n","")
        li_limpio = " ".join(li.split())

        lis.append(li)

    informacion = p_limpio + " -".join(lis)

    contenido.append([tituloDiv, informacion])

    #REVALIDACION
    id = "//*[@id='revalidacion']"

    btn = Wait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='requisito']/div/div[2]/div[1]/div[3]"))
    )
    
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(1)

    subtitulo = driver.find_element(By.XPATH, f"{id}/h2")
    subtitulo = subtitulo.get_attribute("textContent")

    tituloDiv = titulo + " - " + subtitulo
    print(tituloDiv)

    ps = []

    for i in range(5):
        p = driver.find_element(By.XPATH, f"{id}/p[{i+1}]")
        pTexto = p.get_attribute("textContent").strip().replace("\n","")
        p_limpio = " ".join(pTexto.split())

        if i == 3:
            #//*[@id="revalidacion"]/p[4]/a
            p = p.find_element(By.TAG_NAME, "a")
            a = p.get_attribute("href").strip().replace("\n","")
            logitud = len(p_limpio)
            p_limpio = p_limpio[:logitud-2] + ": " + a + ")."

        
        ps.append(p_limpio)
    
    

    informacion = " ".join(ps)

    contenido.append([tituloDiv, informacion])

    #ACTIVIDADES
    #//*[@id="actividadesExtracurriculares"]/div/div[1]/h2
    titulo = driver.find_element(By.XPATH, "//*[@id='actividadesExtracurriculares']/div/div[1]/h2")
    titulo = titulo.get_attribute("textContent")

    cards = driver.find_elements(By.XPATH, "//*[@id='actividadesExtracurriculares']/div/div[2]/*")

    for card in range(len(cards)):
        #//*[@id="actividadesExtracurriculares"]/div/div[2]/div[1]/article/div/div

        elemento = driver.find_element(By.XPATH, f"//*[@id='actividadesExtracurriculares']/div/div[2]/div[{card + 1}]/article/div/div")
        #//*[@id="actividadesExtracurriculares"]/div/div[2]/div[1]/article/div/div/h3
        h3 = elemento.find_element(By.XPATH, ".//h3")
        h3 = h3.get_attribute("textContent")
        print(h3)
        #//*[@id="actividadesExtracurriculares"]/div/div[2]/div[1]/article/div/div/a
        a = elemento.find_element(By.XPATH, ".//a")
        a = a.get_attribute("href")
        print(a)

        informacion = h3 + " | Link para más información: " + a

        contenido.append([titulo, informacion])

    #Generador del archivo
    archivo_csv = "cedi_fca.csv"
    cabeceras = ["Titulo","Información"]

    with open(archivo_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(cabeceras)
        writer.writerows(contenido)
        
    print(f"¡Éxito! Datos guardados correctamente en '{archivo_csv}'")

except Exception as e:
    print(f"Error: {e}")