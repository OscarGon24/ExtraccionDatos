import csv
import time
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains # <- Nueva importación

opciones = Options()

# 1. Configuraciones base de seguridad
opciones.add_argument('--ignore-certificate-errors')
opciones.add_argument('--ignore-ssl-errors')
opciones.set_capability('acceptInsecureCerts', True)

# 2. Desactivar explícitamente el modo HTTPS desde las preferencias internas
prefs = {"https_only_mode_enabled": False}
opciones.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=opciones)

directorio = []

def extraerDirectorio():

    try:
        driver.get("http://intranet.fca.unam.mx/SIDE/")
        time.sleep(2) 

        try:
            ActionChains(driver).send_keys('thisisunsafe').perform()
        except Exception as e:
            pass 

        titulo = driver.find_element(By.XPATH, "/html/body/header/div/div[2]").text
        print(f"Título de la página: {titulo}\n" + "-"*30)

        todos = Wait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='cuerpo']/nav/ul/li[4]/a"))    
        )
        todos.click()

        time.sleep(4)

        letras = driver.find_elements(By.XPATH, "//*[@id='informacion']/div[1]/div[1]/*")
        cantidadLetras = len(letras)
        print(f"Cantidad de letras: {cantidadLetras}")

        for letra in range(cantidadLetras):
            letras_actualizadas = driver.find_elements(By.XPATH, "//*[@id='informacion']/div[1]/div[1]/*")
            nombre_letra = letras_actualizadas[letra].text
            print(f"\n--- Procesando letra {nombre_letra} ---")

            letraElemento = Wait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//*[@id='informacion']/div[1]/div[1]/a[{letra+1}]"))
            )
            letraElemento.click()
            time.sleep(3)
            paginaciones = driver.find_elements(By.XPATH, "//*[@id='paginacion']/*")
            paginacionlista = []
            for i in paginaciones:
                texto = i.text.strip()
                if texto.isdigit():
                    paginacionlista.append(int(texto))

            cantidadPaginaciones = max(paginacionlista) if paginacionlista else 1
            print(f"La letra {nombre_letra} tiene {cantidadPaginaciones} paginaciones.")

            print("Comienza el recorrido de páginas")
            for i in range(1, cantidadPaginaciones + 1):

                if i > 1:
                    paginacion = Wait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, f"//*[@id='paginacion']//a[normalize-space()='{i}']"))
                    )
                    paginacion.click()
                    time.sleep(3)

                print(f"[+] Pagina {i}...")

                tarjetas = driver.find_elements(By.XPATH, "//*[@id='informacion']//div[contains(@class, 'paper_note')]")

                cantidadTarjetas = len(tarjetas)
                print(f"[+]  Cantidad de tarjetas: {cantidadTarjetas}")

                for of in range(cantidadTarjetas):
                    numeroDiv = of + 1
                    datos = driver.find_elements(By.XPATH, f"//*[@id='informacion']/div[1]/div[2]/div[{numeroDiv}]/div/*")
                    cantidadDatos = len(datos)
                    print(f"Cantidad de posibles datos: {cantidadDatos}")

                    oficina = datos[0].text

                    if datos[1].get_attribute("class") == "fila_note_sub":
                        subOficina = datos[1].text
                        cargo = datos[2].text
                        nombre = datos[3].text
                        oficina = f"{oficina} - {subOficina}"
                        contacto = 4
                    else:
                        cargo = datos[1].text
                        nombre = datos[2].text

                        contacto = 3

                    if len(oficina) == 0:
                        oficina = "No se encontró información"
                    elif len(cargo) == 0: 
                        cargo = "No se encontró información"
                    elif len(nombre) == 0:
                        nombre = "No se encontró información"

                    
                    print(f"Oficina: {oficina}")
                    print(f"Cargo: {cargo}")
                    print(f"Nombre: {nombre}")

                    telefonos = []
                    correos = []

                    if cantidadDatos > contacto:

                        for j in range(contacto, cantidadDatos):
                            texto = datos[j].text
                            if "@" in texto:
                                correos.append(texto)
                                print(f"Correo encontrado: {texto}")
                            else:
                                if "\next" in texto:
                                    texto = texto.replace("\next", " ext")
                                    telefonos.append(texto)
                                    print(f"Teléfono encontrado: {texto}")
                                else:
                                    telefonos.append(texto)
                                    print(f"Teléfono encontrado: {texto}")
                    
                    else:
                        print("No se encontraron teléfonos o correos para esta tarjeta.")
                        telefonos.append("No se encontró información")
                        correos.append("No se encontró información")

                    directorio.append([oficina, cargo, nombre, telefonos, correos])

        print(f"Se extrajeron {len(directorio)} contactos.")

        archivo_csv = "directorio_fca.csv"
        cabeceras = ["Oficina", "Cargo", "Nombre", "Teléfonos", "Correos"]

        with open(archivo_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(cabeceras)
            writer.writerows(directorio)
            
        print(f"¡Éxito! Datos guardados correctamente en '{archivo_csv}'")
    except Exception as e:
        print(f"Error durante el proceso: {e}")

    finally:
        print("Cerrando el navegador...")
        driver.quit()
