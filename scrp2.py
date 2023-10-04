import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import Workbook

url = 'https://fbref.com/es/comps/21/horario/Resultados-y-partidos-en-Primera-Division'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

#encuentra todas la tablas de estadisticas
tablas = soup.find_all('table')

#crea un libro en excel
libro = Workbook()

#itero sobre las tablas
for i, tabla in enumerate (tablas):
    filas = tabla.find_all('tr')

    #encabezado de columna
    encabezados = [th.get_text() for th in filas[0].find_all(['th', 'td'])]
    print(f'Tabla {i+1} - Encabezados: {len(encabezados)}')

    #itera sobre las filas y extrae dato
    datos = []
    for fila in filas [1:]:
        fila_datos = [td.get_text() for td in fila.find_all(['th', 'td'])]
        if len(fila_datos) == len(encabezados):
            datos.append(fila_datos)
    print(f'Tabla {i+1} -Datos: {len(datos)} filas')

    #crea un dataframe de pandas con los encabezados y datos
    df = pd.DataFrame(datos, columns=encabezados)

    #crea una hoja en  el libro de excel 
    hoja = libro.create_sheet(title=f'Tabla {i+1}')

    #escribe los encabezados en la hoja
    hoja.append(encabezados)

    for fila in df.values:
        hoja.append(fila.tolist())

#elimina la hoja de inicio predeterminado 
libro.remove(libro['Sheet'])

#guarda el libro de excel
nombre_archivo = 'tablas_pdivision2.xlsx'
libro.save(nombre_archivo)
print(f'Tablas exportadas a {nombre_archivo}')