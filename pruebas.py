def limpiarPrgunta(cadena):
    
    cadenaLimpia = []

    for palabra in cadena:
        palabra = palabra.lower()
        palabrasLimpias = []
        palabraLimpia = ""
        
        for letra in palabra:
            if letra == "á":
                letra = "a"
            elif letra == "é":
                letra = "e"
            elif letra == "í":
                letra = "i"
            elif letra == "ó":
                letra = "o"
            elif letra == "ú":
                letra = "u"
            else:
                letra = letra
            
            palabraLimpia = palabraLimpia + letra
        
        cadenaLimpia.append(palabraLimpia)
        
    print(cadenaLimpia)
    
def limpiarResultados(lista):
    
    signos = ['[', ']', '\'']
    cadenaLimpia = []

    for palabra in lista:
        palabra = palabra.lower()
        palabrasLimpias = []
        palabraLimpia = ""
        
        for letra in palabra:
            if letra == "á":
                letra = "a"
            elif letra == "é":
                letra = "e"
            elif letra == "í":
                letra = "i"
            elif letra == "ó":
                letra = "o"
            elif letra == "ú":
                letra = "u"
            elif letra in signos:
                letra = letra.replace(letra, "")
            else:
                letra = letra
            
            palabraLimpia = palabraLimpia + letra
        print(palabraLimpia)
        cadenaLimpia.append(palabraLimpia)
        
    #print(cadenaLimpia)
        
        
    
##############################

listaPalabras = ['quien', 'es', 'el', 'jefe', 'de', 'la', 'Licenciatura', 'en', 'informática']
resultados = "['En la oficina de División de Estudios de Posgrado, el contacto es Clotilde Hernández Garnica con el cargo de Coordinadora del Programa de Posgrado en Ciencias de la Administración. Su teléfono es (55) 5622 8474 y su correo electrónico es chernan@posgrado.unam.mx.', 'En la oficina de Coordinación del Programa de Posgrado en Ciencias de la Administración, el contacto es Leticia Estrada Martínez con el cargo de Apoyo del Doctorado en Ciencias de la Administración. Su teléfono es (55) 5616 0311 y su correo electrónico es ppca_doctorado@posgrado.unam.mx.', 'En la oficina de Centro de Informática - Capacitación Especializada en TIC, el contacto es Rocío Aymé García Castillo con el cargo de Coordinadora de Capacitación Especializada en TIC (CETIC) y Laboratorios de Cómputo. Su teléfono es (55) 5622 8422 y su correo electrónico es cetic@fca.unam.mx, rgarcia@fca.unam.mx.', 'En la oficina de División de Estudios de Posgrado, el contacto es María Columba Pérez Maciel con el cargo de Apoyo del Doctorado en Ciencias de la Administración. Su teléfono es 5616 0311 y su correo electrónico es columbaperez@fca.unam.mx.', 'En la oficina de División de Estudios de Posgrado, el contacto es Luis Alberto Gómez Alvarado con el cargo de Coordinador de las Especialidades en Alta Dirección, Recursos Humanos y Mercadotecnía. Su teléfono es 5622 8452 y su correo electrónico es lgomez@fca.unam.mx.', 'En la oficina de División de Estudios de Posgrado, el contacto es Jorge Armando Arrioja Pardo con el cargo de Apoyo a Coordinación de la Maestría en Administración de las Organizaciones Tecnología y Contribuciones. Su teléfono es (55) 5622 8357, (55) 5622 8454 y su correo electrónico es jpardo@fca.unam.mx.', 'En la oficina de División de Estudios de Posgrado, el contacto es María Eugenia Miranda Jaimes con el cargo de Coordinadora de la Maestría en Administración de las Organizaciones, Tecnología y Contribuciones. Su teléfono es (55) 5622 8357, (55) 5622 8454 y su correo electrónico es mmiranda@fca.unam.mx.', 'En la oficina de Secretaría Divulgación y Fomento Editorial, el contacto es César David Cristobal Suaste con el cargo de Técnico en Imprenta. Su teléfono es 5622 8402 y su correo electrónico es [].', 'En la oficina de Secretaría de Relaciones y Extensión Universitaria - Unidad Integral de Género, el contacto es Blanca Elizabeth Jiménez Cruz con el cargo de Coordinadora Clínica del Centro de Orientación Educativa (COE). Su teléfono es (55) 5616 0823 ext. 102, (55) 5616 2965 ext. 102 y su correo electrónico es bjimenez@fca.unam.mx.', 'En la oficina de Centro de Informática - Coordinación de Laboratorios, el contacto es Sergio Iván Martínez Pichardo con el cargo de Apoyo a Laboratorios de Cómputo. Su teléfono es 5623 7000 y su correo electrónico es imartinez@fca.unam.mx.']"

resultados = resultados.lower()

#limpiarPrgunta(listaPalabras)
limpiarResultados(resultados)
