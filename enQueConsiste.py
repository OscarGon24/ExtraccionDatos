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

def Extractor(link, titulacion, id):

    driver.get(link)
    time.sleep(1)

    print(titulacion)

    try:
        
        texto = driver.find_element(By.ID, f"{id}").text.strip().replace("\n","")
        return texto

    except Exception as e:
        print(f"Error durante el proceso: {e}")

def ExtractorTextoInscripcion(id, nombre):

    textoFinal = ""

    tabTexto = driver.find_element(By.ID, f"{id}").get_attribute("textContent").strip()
                            
    tabTextoLimpio = " ".join(tabTexto.split())
    textoFinal += f"[[[{nombre}]]] {tabTextoLimpio} "

    print(textoFinal + "\n"*2)
    
    return textoFinal



def inscripcion(link, titulacion):
    
    driver.get(link)
    time.sleep(1)

    print(titulacion)

    try:
        #Extraee los tab del content
        todasTarjetas = driver.find_elements(By.XPATH, "//*[@id='tab3']/li")
        #Se queda con los que estan en la pagina
        tarjetasReales = [tarjeta for tarjeta in todasTarjetas if tarjeta.is_displayed()]
        
        print(f"Pestañas reales: {len(tarjetasReales)}")

        if "especializacion" in link:

            ExtractorTextoInscripcion("inscripcion", "Procedimiento de inscripción")
        
        else:
            for tarjeta in tarjetasReales:
                # Convertimos el nombre a MAYÚSCULAS para que las validaciones nunca fallen
                nombre = tarjeta.get_attribute("textContent").strip().upper()
                print(f"Procesando pestaña: {nombre}")

                if "FCA-UNAM" in nombre:

                    if "diplomado_linea" in link or "diplomado_ingles" in link:
                        ExtractorTextoInscripcion("inscripcion_fca", nombre)
                    else:
                        ExtractorTextoInscripcion("webdesign", nombre)

                elif "INSTITUCIONES INCORPORADAS" in nombre or "INCORPORADAS" in nombre:

                    if "diplomado_presencial" in link:
                        ExtractorTextoInscripcion("consulting",nombre)

                    elif "diplomado_linea" in link or "diplomado_ingles" in link:
                        ExtractorTextoInscripcion("inscripcion_inc",nombre)
                    
                    else:
                        ExtractorTextoInscripcion("coding",nombre)

                elif "OTRAS FACULTADES UNAM" in nombre or "FACULTADES Y FES-UNAM" in nombre:

                    if "diplomado_linea" in link or "diplomado_ingles" in link:
                        ExtractorTextoInscripcion("inscripcion_fes",nombre)

                    else:
                        ExtractorTextoInscripcion("coding",nombre)

                elif "RECURSAMIENTO" in nombre:

                    if "diplomado_linea" in link or "diplomado_ingles" in link:
                        ExtractorTextoInscripcion("inscripcion_rec",nombre)

                    else:
                        ExtractorTextoInscripcion("inscripcion_rec",nombre)

                elif "EX-ALUMNOS UNAM" in nombre:
                    ExtractorTextoInscripcion("inscripcion_exa", nombre)

                elif "EXTERNOS A LA UNAM" in nombre:
                    ExtractorTextoInscripcion("inscripcion_ext", nombre)

                else: 
                    print("Otro")
         

    except Exception as e:
        print(f"Error durante el proceso: {e}")
        return "No aplica"

try:

    df = pd.read_csv("titulacion_fca.csv")
    listaLinks = df["Link"].tolist()[6:]
    listaTitulacion = df["Titulación"].tolist()[6:]

    textosExtraidos = ["No aplica","No aplica","No aplica","No aplica","No aplica","No aplica"]

    for link,titulacion in zip(listaLinks,listaTitulacion):
        if "#consiste" in link:
            id="consiste"
            texto = Extractor(link,titulacion,id)
            textosExtraidos.append(texto)
        elif "#inscripcion" in link:
            texto = inscripcion(link,titulacion)
            textosExtraidos.append(texto)
        else:
            textosExtraidos.append("No aplica")

    df["Informacion"] = textosExtraidos
    df.to_csv("titulacion_fca.csv", index=False, encoding='utf-8')
    print("\n¡Proceso terminado! Se actualizó el archivo 'titulacion_fca.csv' con la nueva columna.")


except Exception as e:
    print(f"Error durante el proceso: {e}")

finally:
    driver.quit()