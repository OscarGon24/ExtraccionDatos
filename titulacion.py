import csv
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

directorio = []
navbarDatos = []

def datosNavbar():

    xpath = "//*[@id='navbar-full-demo']"
    navbarElementos = driver.find_elements(By.XPATH, f"{xpath}/*")
    print(len(navbarElementos))

    for elemento in range(len(navbarElementos)):#//*[@id="navbar-full-demo"]/ul[2]/li/a

        #Reglamento
        if elemento == 0:

            navbarElemento = driver.find_element(By.XPATH, f"{xpath}/ul[{elemento+1}]/a")
            nombre = navbarElemento.get_attribute("textContent").strip().replace("\n","")
            link= navbarElemento.get_attribute("href")
            print(f"{nombre}: {link}")

            navbarDatos.append(["Reglamento",nombre,link])

        #Diplomado
        elif elemento == 2:#//*[@id="navbar-full-demo"]/ul[3]/li/ul

            navbarElemento = driver.find_element(By.XPATH, f"{xpath}/ul[{elemento+1}]/li/a")
            nombre = navbarElemento.get_attribute("textContent").strip().replace("\n","")
            print("-"*30 + "\n" + f"{nombre}")

            navbarElementoLista = driver.find_elements(By.XPATH, f"{xpath}/ul[{elemento+1}]/li/ul/*")
            print(f"Sub-Elementos: {len(navbarElementoLista)}")

            for item in range(len(navbarElementoLista)):#//*[@id="navbar-full-demo"]/ul[3]/li/ul/li[1]/a
                navbarElemento = driver.find_element(By.XPATH, f"{xpath}/ul[{elemento+1}]/li/ul/li[{item+1}]/a")
                nombre = navbarElemento.get_attribute("textContent").strip().replace("\n","")
                print("-"*30 + f"\n{nombre}")

                navbarSubElementosLista = driver.find_elements(By.XPATH, f"{xpath}/ul[{elemento+1}]/li/ul/li[{item+1}]/ul/*")
                print(f"Sub-Elementos Internos: {len(navbarSubElementosLista)}")

                for sub in range(len(navbarSubElementosLista)):#//*[@id="navbar-full-demo"]/ul[3]/li/ul/li[1]/ul/li[1]/a
                    navbarElemento = driver.find_element(By.XPATH, f"{xpath}/ul[{elemento+1}]/li/ul/li[{item+1}]/ul/li[{sub+1}]/a")
                    categoria = navbarElemento.get_attribute("textContent").strip().replace("\n","")
                    link= navbarElemento.get_attribute("href")
                    print(f"{nombre}-{categoria}: {link}")

                    navbarDatos.append([nombre, categoria, link])

        #Todos los demás
        else:#//*[@id="navbar-full-demo"]/ul[2]/li/ul

            navbarElemento = driver.find_element(By.XPATH, f"{xpath}/ul[{elemento+1}]/li/a")
            nombre = navbarElemento.get_attribute("textContent").strip().replace("\n","")
            print("-"*30 + "\n" + f"{nombre}")

            navbarElementoLista = driver.find_elements(By.XPATH, f"{xpath}/ul[{elemento+1}]/li/ul/*")
            print(len(navbarElementoLista))

            for item in range(len(navbarElementoLista)):#//*[@id="navbar-full-demo"]/ul[2]/li/ul/li[1]/a
                navbarElemento = driver.find_element(By.XPATH, f"{xpath}/ul[{elemento+1}]/li/ul/li[{item+1}]/a")
                categoria = navbarElemento.get_attribute("textContent").strip().replace("\n","")
                link= navbarElemento.get_attribute("href")
                print(f"{nombre}-{categoria}: {link}")

                navbarDatos.append([nombre, categoria, link])

def convocatoriasParaInscripcion():

    xpath = "/html/body/section/div/div[1]"

    elementos = driver.find_elements(By.XPATH, f"{xpath}/*")
    print(len(elementos))

    for elemento in range(len(elementos)):#/html/body/section/div/div[1]/div[1]/div/div[2]/h3

        #Mostrados en pantalla

        item = driver.find_element(By.XPATH, f".//div[{elemento+1}]/div/div[2]/h3")
        titulacion = item.get_attribute("textContent").strip().replace("\n","")

        item = driver.find_element(By.XPATH, f".//div[{elemento+1}]/div/div[2]/p")
        periodo = item.get_attribute("textContent").strip().replace("\n","")[21:]
        print(f"{titulacion}: {periodo}")

        #Ocultos /html/body/section/div/div[1]/div[1]/div/div[1]/div/ul
        itemsOcultos = driver.find_elements(By.XPATH, f"{xpath}/div[{elemento+1}]/div/div[1]/div/ul/*")
        print(len(itemsOcultos))

        try:
            for oculto in range(len(itemsOcultos)):
                item = driver.find_element(By.XPATH, f"{xpath}/div[{elemento+1}]/div/div[1]/div/ul/li[{oculto+1}]/a")
                link = item.get_attribute("href").strip()

                if ".php#" in link:
                    consiste = link
                else:
                    if "jpg" in link or "png" in link:
                        link = link
                        categoria = "Imagen"
                    else:
                        link = link
                        categoria = "PDF"
        except Exception as e:
            print(f"[-] No funciona un link de {titulacion}, tiene {len(itemsOcultos)}")
            continue

        

try:
    url = "https://titulacion.fca.unam.mx/"
    driver.get(url)

    #datosNavbar()
    convocatoriasParaInscripcion()

except Exception as e:
    print(f"Error durante el proceso: {e}")

finally:
    print("Cerrando el navegador...")
    driver.quit()
