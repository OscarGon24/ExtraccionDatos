import time
import directorio
import licenciaturas
import titulacion
import extractorTitulacion
import servicioSocial
import becas
from selenium import webdriver

print("Iniciando extracción de datos...\n")
try:
    print("Extrayendo directorio...")
    directorio.extraerDirectorio()
    time.sleep(30)

except Exception as e:
    print(f"Error durante el proceso: {e}")

finally:
    print("Cerrando el navegador...")
    driver.quit()

try:
    print("Extrayendo oferta educativa licenciaturas...")
    licenciaturas.extraerLicenciaturas()
    time.sleep(30)

except Exception as e:
    print(f"Error durante el proceso: {e}")

finally:
    print("Cerrando el navegador...")
    driver.quit()

try:
    print("Extrayendo datos de la titulación...")
    titulacion.datosNavbar()
    titulacion.convocatoriasParaInscripcion()
    time.sleep(30)

except Exception as e:
    print(f"Error durante el proceso: {e}")

finally:
    print("Cerrando el navegador...")
    driver.quit()

try:
    print("Extrayendo datos del Servicio Social...")
    servicioSocial()
    time.sleep(30)

except Exception as e:
    print(f"Error durante el proceso: {e}")

finally:
    print("Cerrando el navegador...")
    driver.quit()

try:
    print("Extrayendo datos de las becas...")
    becas()
    time.sleep(30)

except Exception as e:
    print(f"Error durante el proceso: {e}")

finally:
    print("Cerrando el navegador...")
    driver.quit()