import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

datos = []

def extraerLicenciaturas():

    try:
        driver.get("https://licenciaturas.fca.unam.mx")
        time.sleep(5)

        titulo = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/h2").text
        print(f"Título de la página: {titulo}\n" + "-"*30)

        ids = ["conta", "admin", "info", "negocios"]

        for id in ids:
            
            if id == "negocios":
                licenciatura = driver.find_element(By.XPATH, f"//*[@id='{id}']/div/div[1]/div/div[1]/div/h1")
                licenciatura = licenciatura.get_attribute("textContent").strip()

                perfil = driver.find_element(By.XPATH, f"//*[@id='perfil']/p")
                perfilInfo = perfil.get_attribute("textContent").strip()


                actitudes = driver.find_element(By.XPATH, f"//*[@id='actitudes']/ul")
                actitudesInfo = []
                for li in actitudes.find_elements(By.TAG_NAME, "li"):
                    actitudesInfo.append(li.get_attribute("textContent").strip())

                conocimientos = driver.find_element(By.XPATH, f"//*[@id='conocimientos']/ul")
                conocimientosInfo = []
                for li in conocimientos.find_elements(By.TAG_NAME, "li"):
                    conocimientosInfo.append(li.get_attribute("textContent").strip())

                habilidades = driver.find_element(By.XPATH, f"//*[@id='habilidades']/ul")
                habilidadesInfo = []
                for li in habilidades.find_elements(By.TAG_NAME, "li"):
                    habilidadesInfo.append(li.get_attribute("textContent").strip())
            else:
                licenciatura = driver.find_element(By.XPATH, f"//*[@id='{id}']/div/div[1]/div/div[1]/div/h1")
                licenciatura = licenciatura.get_attribute("textContent").strip()

                perfil = driver.find_element(By.XPATH, f"//*[@id='{id}-perfil']/p")
                perfilInfo = perfil.get_attribute("textContent").strip()

                actitudes = driver.find_element(By.XPATH, f"//*[@id='{id}-actitudes']/ul")
                actitudesInfo = []
                for li in actitudes.find_elements(By.TAG_NAME, "li"):
                    actitudesInfo.append(li.get_attribute("textContent").strip())

                conocimientos = driver.find_element(By.XPATH, f"//*[@id='{id}-conocimientos']/ul")
                conocimientosInfo = []
                for li in conocimientos.find_elements(By.TAG_NAME, "li"):
                    conocimientosInfo.append(li.get_attribute("textContent").strip())

                habilidades = driver.find_element(By.XPATH, f"//*[@id='{id}-habilidades']/ul")
                habilidadesInfo = []
                for li in habilidades.find_elements(By.TAG_NAME, "li"):
                    habilidadesInfo.append(li.get_attribute("textContent").strip())

            datos.append(["Oferta Educativa", licenciatura, perfilInfo, actitudesInfo, conocimientosInfo, habilidadesInfo])

        print(f"Se extrajeron {len(datos)} carreras/cursos.")

        archivo_csv = "oferta_educativa_fca.csv"
        cabeceras = ["Seccion", "Licenciatura", "Perfil", "Actitudes", "Conocimientos", "Habilidades"]

        with open(archivo_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(cabeceras)
            writer.writerows(datos)
            
        print(f"¡Éxito! Datos guardados correctamente en '{archivo_csv}'")

    except Exception as e:
        print(f"Error durante el proceso: {e}")

    finally:
        print("Cerrando el navegador...")
        driver.quit()