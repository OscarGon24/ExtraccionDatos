import csv
import time
import directorio
import licenciaturas
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

print("Iniciando extracción de datos...\n")
try:
    print("Extrayendo directorio...")
    directorio.extraerDirectorio()

except Exception as e:
    print(f"Error durante el proceso: {e}")

finally:
    print("Cerrando el navegador...")
    driver.quit()

try:
    print("Extrayendo oferta educativa licenciaturas...")
    licenciaturas.extraerLicenciaturas()

except Exception as e:
    print(f"Error durante el proceso: {e}")

finally:
    print("Cerrando el navegador...")
    driver.quit()