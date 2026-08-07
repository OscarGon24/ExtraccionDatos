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
        print(f"Error durante extraccion de consiste: {e}")

def ExtractorTextoInscripcion(id, nombre):

    textoFinal = ""

    tabTexto = driver.find_element(By.ID, f"{id}").get_attribute("textContent").strip()
                            
    tabTextoLimpio = " ".join(tabTexto.split())
    textoFinal += f"[[[{nombre}]]] {tabTextoLimpio} "

    #print(textoFinal + "\n"*2)
    
    return textoFinal

def inscripcion(link, titulacion):
    
    driver.get(link)
    time.sleep(1)

    #print(titulacion)

    try:
        todasTarjetas = driver.find_elements(By.XPATH, "//*[@id='tab3']/li")
        tarjetasReales = [tarjeta for tarjeta in todasTarjetas if tarjeta.is_displayed()]
        
        #print(f"Pestañas reales: {len(tarjetasReales)}")

        textoFinal = ""

        if "especializacion" in link or "universidad_extranjera" in link:

            textoFinal +=ExtractorTextoInscripcion("inscripcion", "Procedimiento de inscripción")
        
        else:
            for tarjeta in tarjetasReales:
                nombre = tarjeta.get_attribute("textContent").strip().upper()
                #print(f"Procesando pestaña: {nombre}")

                if "FCA-UNAM" in nombre or "FCA - UNAM" in nombre:

                    if "diplomado_linea" in link or "diplomado_ingles" in link:
                        textoFinal +=ExtractorTextoInscripcion("inscripcion_fca", nombre)
                    else:
                        textoFinal +=ExtractorTextoInscripcion("webdesign", nombre)

                elif "INSTITUCIONES INCORPORADAS" in nombre or "INCORPORADAS" in nombre:

                    if "diplomado_presencial" in link:
                        textoFinal +=ExtractorTextoInscripcion("consulting",nombre)

                    elif "diplomado_linea" in link or "diplomado_ingles" in link:
                        textoFinal +=ExtractorTextoInscripcion("inscripcion_inc",nombre)
                    
                    else:
                        textoFinal +=ExtractorTextoInscripcion("coding",nombre)

                elif "OTRAS FACULTADES UNAM" in nombre or "FACULTADES Y FES-UNAM" in nombre:

                    if "diplomado_linea" in link or "diplomado_ingles" in link:
                        textoFinal +=ExtractorTextoInscripcion("inscripcion_fes",nombre)

                    else:
                        textoFinal +=ExtractorTextoInscripcion("coding",nombre)

                elif "RECURSAMIENTO" in nombre:

                    if "diplomado_linea" in link or "diplomado_ingles" in link:
                        textoFinal +=ExtractorTextoInscripcion("inscripcion_rec",nombre)

                    else:
                        textoFinal +=ExtractorTextoInscripcion("inscripcion_rec",nombre)

                elif "EX-ALUMNOS UNAM" in nombre:
                    textoFinal +=ExtractorTextoInscripcion("inscripcion_exa", nombre)

                elif "EXTERNOS A LA UNAM" in nombre:
                    textoFinal +=ExtractorTextoInscripcion("inscripcion_ext", nombre)

                elif "REINSCRIPCIÓN Y PRÓRROGA" in nombre:
                    textoFinal +=ExtractorTextoInscripcion("coding", nombre)

                elif "INSCRIPCIÓN" in nombre:

                    if "tesis" in link:
                        textoFinal +=ExtractorTextoInscripcion("webdesign", nombre)
                    else:
                        textoFinal +=ExtractorTextoInscripcion("inscripcion", nombre)

                elif "ACREDITACIÓN" in nombre:

                    if "tesis" in link:
                        textoFinal +=ExtractorTextoInscripcion("consulting", nombre)
                    else:
                        textoFinal +=ExtractorTextoInscripcion("coding", nombre)

                else: 
                    #print("Otro")
                    return "No aplica"

        return textoFinal.strip()
         

    except Exception as e:
        print(f"Error durante extraccion de inscripciones: {e}")
        return "No aplica"

def convocatoriaTitulo(link, titulacion):

    try:
        driver.get(link)
        time.sleep(1)

        #print(titulacion)

        if "Diseño" in titulacion or "Diplomado" in titulacion or "Interfacultades" in titulacion or "Extranjera" in titulacion or "Tesis" in titulacion or "Servicio" in titulacion:
            xpath = "//*[@id='convocatoria_po']/section/div/div"

        elif "Especialización" in titulacion:
            xpath = "//*[@id='convocatoria']/section/div/div"

        else:
            xpath = "//*[@id='convocatoria_titulo']/section/div/div"

        h2 = driver.find_element(By.XPATH, f"{xpath}/h2")
        h2Texto = h2.get_attribute("textContent").strip()

        #print(h2Texto)

        textoFinal = ""

        if "Actualmente no hay convocatorias" in h2Texto:
            return h2Texto
        
        else:

            iconos = driver.find_elements(By.XPATH, f"{xpath}//a")
            #print(f"Cantidad de iconos: {len(iconos)}")

            for icono in iconos:
                nombre = icono.get_attribute("textContent").strip()
                link = icono.get_attribute("href").strip()
                textoFinal += f"Para la {nombre} el link es: {link} "

            #print(textoFinal + "\n")
            return textoFinal

    except Exception as e:
            print(f"Error durante extraccion de convocatorias: {e}")
            return "No aplica"

def horarios(link, titulacion):
    try:
        driver.get(link)
        time.sleep(1)

        #print(titulacion)

        if "diplomado_linea" in link or "diplomado_ingles" in link:
            xpathTabla = "//*[@id='horarios']/table"
        else:
            xpathTabla = "//*[@id='horarios']/div/div/table"

        tablas = driver.find_elements(By.XPATH, xpathTabla)

        textoFinal = ""

        if len(tablas) == 0:
            texto = driver.find_element(By.XPATH, "//*[@id='horarios']/div/div/p")
            textoFinal = texto.get_attribute("textContent").strip()
            return textoFinal
            
        else:
            tabla_encontrada = tablas[0]
            filas = tabla_encontrada.find_elements(By.TAG_NAME, "tr")
            
            textosExtraidos = []

            for fila in filas:
                celdas = fila.find_elements(By.TAG_NAME, "td")

                if "diplomado_linea" in link:

                    if len(celdas) > 0:
                                            
                        diplomado = celdas[0].get_attribute("textContent").strip()
                        grupo = celdas[1].get_attribute("textContent").strip()
                        inicio = celdas[2].get_attribute("textContent").strip()
                        status = celdas[3].get_attribute("textContent").strip()
                        disponibilidad = celdas[4].get_attribute("textContent").strip()

                        
                        oracion = f"El diplomado {diplomado} (Grupo {grupo}) inicia tentativamente el {inicio}. Estatus: {status}. {disponibilidad} tiene lugares disponibles."
                        
                        textosExtraidos.append(oracion)

                else:
                    if len(celdas) > 0:
                        
                        diplomado = celdas[0].get_attribute("textContent").strip()
                        grupo = celdas[1].get_attribute("textContent").strip()
                        inicio = celdas[2].get_attribute("textContent").strip()
                        dias = celdas[3].get_attribute("textContent").strip()
                        horario = celdas[4].get_attribute("textContent").strip()
                        salon = celdas[5].get_attribute("textContent").strip()
                        status = celdas[6].get_attribute("textContent").strip()
                        disponibilidad = celdas[7].get_attribute("textContent").strip()
                        
                        oracion = f"El diplomado {diplomado} (Grupo {grupo}) inicia tentativamente el {inicio}. Las clases son {dias} en horario de {horario} en el salón {salon}. Estatus: {status}. {disponibilidad} tiene lugares disponibles."
                        
                        textosExtraidos.append(oracion)

            textoFinal = " | ".join(textosExtraidos)
            return textoFinal

    except Exception as e:
        print(f"Error durante extraccion de horarios: {e}")
        return "No aplica"

def temario(link, titulacion):

    driver.get(link)
    time.sleep(1)

    xpath = "//*[@id='temarios']/section/div/div/div"

    textoFinal = ""
    textosExtraidos = []

    try:

        iconos = driver.find_elements(By.XPATH, f"{xpath}//a")
        #print(f"Cantidad de iconos: {len(iconos)}")

        for icono in iconos:
            nombre = icono.get_attribute("textContent").strip()
            link = icono.get_attribute("href").strip()
            oracion = f"Para el curso {nombre}  el temario esta en el link: {link} "
            textosExtraidos.append(oracion)

        textoFinal = " | ".join(textosExtraidos)
        #print(textoFinal + "\n")
        return textoFinal

    except Exception as e:
        print(f"Error durante extraccion de temarios: {e}")
        return "No aplica"

def asesores(link, titulacion):

    driver.get(link)
    time.sleep(1)

    textoFinal = ""
    textosExtraidos = []

    try:
        paneles = driver.find_elements(By.XPATH, "//*[@id='tab2Content']/div[contains(@class, 'tab-pane')]")
        
        for panel in paneles:
            idPanel = panel.get_attribute("id")
            
            if idPanel == "admon":
                nombreLic = "Administración"
            elif idPanel == "conta":
                nombreLic = "Contaduría"
            elif idPanel == "info":
                nombreLic = "Informática"
            elif idPanel == "ni":
                nombreLic = "Negocios Internacionales"
            else:
                nombreLic = idPanel
                
            areas = panel.find_elements(By.XPATH, ".//div[contains(@class, 'accordion-item')]")
            
            for area in areas:
                nombreArea = area.find_element(By.XPATH, ".//h5/button").get_attribute("textContent").strip()
                
                asesores = area.find_elements(By.XPATH, ".//div[contains(@class, 'accordion-body')]//li/a")
                
                for asesor in asesores:
                    nombreAsesor = asesor.get_attribute("textContent").strip()
                    linkPdf = asesor.get_attribute("href")
                    
                    oracion = f"En la licenciatura de {nombreLic}, para el área de {nombreArea}, el asesor es {nombreAsesor}. Ficha técnica: {linkPdf}."
                    
                    textosExtraidos.append(oracion)

        textoFinal = " | ".join(textosExtraidos)
        return textoFinal

    except Exception as e:
        print(f"Error durante el extracción de asesores: {e}")
        return "No aplica"

def lineamientos(link, titulacion):
    driver.get(link)
    time.sleep(1)

    #print(titulacion)
    
    textoFinal = ""
    oraciones_rag = []

    try:
        contenedor = driver.find_element(By.ID, "lineamientos")
        tablas = contenedor.find_elements(By.TAG_NAME, "table")
        for tabla in tablas:
            filas = tabla.find_elements(By.TAG_NAME, "tr")
            for fila in filas:
                celdas = fila.find_elements(By.XPATH, ".//td | .//th")
                if len(celdas) >= 2:
                    estructura = " ".join(celdas[0].get_attribute("textContent").split())
                    descripcion = " ".join(celdas[1].get_attribute("textContent").split())
                    
                    if estructura.upper() != "ESTRUCTURA": 
                        oracion = f"[[[ESTRUCTURA DEL TRABAJO]]] En el apartado de '{estructura}' se requiere: {descripcion}."
                        oraciones_rag.append(oracion)
        acordeones = contenedor.find_elements(By.XPATH, ".//div[contains(@class, 'accordion-item')]")
        for acordeon in acordeones:
            try:
                titulo = acordeon.find_element(By.XPATH, ".//h5/button").get_attribute("textContent").strip()
                contenido = acordeon.find_element(By.XPATH, ".//div[contains(@class, 'accordion-body')]").get_attribute("textContent")
                contenido_limpio = " ".join(contenido.split())
                
                oracion = f"[[[DETALLES DE SECCIÓN]]] Respecto a '{titulo}': {contenido_limpio}"
                oraciones_rag.append(oracion)
            except:
                continue
        texto_bruto = contenedor.get_attribute("textContent")
        texto_limpio = " ".join(texto_bruto.split())
        oraciones_rag.append(f"[[[REGLAS GENERALES]]] {texto_limpio}")

        textoFinal = " | ".join(oraciones_rag)
        return textoFinal

    except Exception as e:
        print(f"Error extrayendo lineamientos: {e}")
        return "No aplica"

def extraerDatosTitulacion():
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
        elif "#convocatoria_titulo" in link or "#convocatoria_po" in link or "#convocatoria" in link:
            texto = convocatoriaTitulo(link,titulacion)
            textosExtraidos.append(texto)
        elif "#procedimiento_titulo" in link:
            texto = inscripcion(link,titulacion)
            textosExtraidos.append(texto)
        elif "#horarios" in link:
            texto = horarios(link,titulacion)
            textosExtraidos.append(texto)
        elif "#temarios" in link:
            texto = temario(link,titulacion)
            textosExtraidos.append(texto)
        elif "#procedimiento_po" in link:
            if "Tesis" in titulacion or "Interfacultades" in titulacion or "Servicio" in titulacion:
                texto = ExtractorTextoInscripcion("procedimiento_po","Procedimiento de prueba oral")
                textosExtraidos.append(texto)
            else:
                texto = inscripcion(link,titulacion)
                textosExtraidos.append(texto)
        elif "#plataforma" in link:
            texto = convocatoriaTitulo(link,titulacion)
            textosExtraidos.append(texto)
        elif "#asesores" in link:
            texto = asesores(link,titulacion)
            textosExtraidos.append(texto)
        elif "#lineamientos" in link:
            texto = lineamientos(link,titulacion)
            textosExtraidos.append(texto)
        else:
            textosExtraidos.append("No aplica")

    df["Informacion"] = textosExtraidos
    df.to_csv("titulacion_fca.csv", index=False, encoding='utf-8')
    print("\n¡Proceso terminado! Se actualizó el archivo 'titulacion_fca.csv' con la nueva columna.")

try:

    extraerDatosTitulacion()

except Exception as e:
    print(f"Error durante el proceso: {e}")

finally:
    driver.quit()