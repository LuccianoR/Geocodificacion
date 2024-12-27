#%% Importo las librerías necesarias par ala geocodificación.

import webbrowser
import pandas as pd
import numpy as np
import requests
import folium
import time
from matplotlib.path import Path

#%% Preparación de los datos.

"""

La idea es realizar funciones que permitan preparar los datos para una geocodificación
correcta y rápida. Principalmente se buscará dividir la base de datos para no
saturar la API.

"""

#Divide un df en sub_dfs de menor cantidad de filas.
def dividir_dataframe(df, max_filas):
    
    #Creamos la lista con los sub_dfs.
    sub_dfs = []
    
    #Asignamos a total_filas el largo de nuestro df original.
    total_filas = len(df)
    
    #Iteramos un rango que va de 0 al máximo de filas del df original (salteando nuestro límite en los sub_dfs).
    for inicio in range(0, total_filas, max_filas):
        
        #Igualamos la variable a la porción del df original que se introducirá en este sub_df.
        #Utilizamos min para el caso donde la suma del índice de inicio mas el máximo de filas sobrepase al total de filas del df.
        #Min nos sirve para poder contemplar los casos donde el último sub_df no complete el límite asignado y se quede corto.
        sub_df = df.iloc[inicio : min(inicio + max_filas, total_filas)].copy()
        
        #Agregamos los sub_dfs a la lista original que nos devolverá la función.
        sub_dfs.append(sub_df)
    
    return sub_dfs


#Guarda los sub_dfs que se encuentran en una lista en archivos .csv para su posterior uso.
def guardar_lista(lista):
    
    #Itera un rango que va de 0 al máximo de elementos de la lista.
    for i in range(0, len(lista)):
        
        #Crea una variable para cada sub_df de la lista.
        df = lista[i]
        
        #Guarda cada sub_df en el repositorio actual.
        df.to_csv(f"df_{i + 1}.csv", index=False)
        
    return

#%% Geocodificacion con el servicio de Here Api

#Realiza peticiones a la api de "Here Api" para obtener un df con dos columnas extras, la de latitud y longitud.
#El utilizar el mismo Df para el guardado de los datos nos permitirá utilizar el resto de las columnas para graficar en el mapa.
def latitud_longitud(df,nombre_archivo, key_api):
    
    #Utilizamos una copia del df para evitar errores.
    df_1 = df.copy()
    
    #Le creamos dos columnas a la copia.
    df_1.loc[:, 'Latitud'] = None
    df_1.loc[:, 'Longitud'] = None
    
    #Iteramos sobre cada fila del df con el método iterrows().
    for index, row in df_1.iterrows():
        
        #Aca igualamos la variable dirección con el dato de la columna "Domicilio".
        #Esta función contempla el df particular que estoy trabajando.
        direccion = row["Domicilio"]
        try:
            
            #Igualamos a la variable la url de consultas de la API.
            url = f"https://geocode.search.hereapi.com/v1/geocode?q={direccion}&apiKey={key_api}"
            
            #Realizamos las consultas con un tiempo máximo de 10 segundos.
            respuesta = requests.get(url, timeout=10)
            
            #Igualamos a la variable la información de la consulta
            data = respuesta.json()
            
            #Veremos si efectivamente se logró hacer la geocodificación.
            #Verificamos si data contiene una lista llamada items y si no está vacía.
            if "items" in data and len(data["items"]) > 0:
                
                #igualamos la posición del objeto a la variable.
                locacion = data["items"][0]["position"]
                
                #Agregamos los datos de latitud y longitud al df con las columnas extras.
                df_1.loc[index, 'Latitud'] = locacion['lat']
                df_1.loc[index, 'Longitud'] = locacion['lng']
           
            #En el caso de que no se haya podido geocodificar.
            else:
                
                #Agregamos el valor nulo a las columnas extras.
                df_1.loc[index, 'Latitud'] = None
                df_1.loc[index, 'Longitud'] = None
                
        #En el caso de error en la geocodificación.
        except requests.exceptions.Timeout:
            print(f"Timeout en la geocodificación de la dirección: {direccion}")
            
            #Agregamos el valor nulo a las columnas extras.
            df_1.loc[index, 'Latitud'] = None
            df_1.loc[index, 'Longitud'] = None
        
        #Esperamos un segundo para hacer la siguiente petición
        #con el fin de no saturar la API.
        time.sleep(1)
        
        print(index)
    
    #Guardamos este nuevo df con el nombre introducido en la llamada a la función
    df_1.to_csv(nombre_archivo, index=False)
    print(f"Archivo guardado como: {nombre_archivo}")
    
    return df_1

#%% Graficar mapa interactivo.
#Esta función está adaptada al uso particular de mi base de datos.


#Genera y abre un archivo HTML con las direcciones en el mapa y sus respectivos datos.
def graficas(df,nombre_archivo, direccion):
    
    #Creamos la variable que contiene el mapa centrado en la ubicación indicada.
    map_ba = folium.Map(location=[-34.6099, -58.4034], zoom_start=15)

    #Iteramos cada fila con el método iterrows() despreciando el índice.
    for _, row in df.iterrows():
        
        #Nos aseguramos que la latitud y longitud no son nulas.
        if not pd.isnull(row['Latitud']) and not pd.isnull(row['Longitud']):
            
            #Llamamos a los datos que nos interesan de cada ubicación.
            popup_text = (
                    f"<strong>Circuito:</strong> {row['Circuito']}<br>"
                    f"<strong>Descripción:</strong> {row['Domicilio']}<br>"
                    f"<strong>Tipo de Documento:</strong> {row['Tipo documento']}<br>"
                    f"<strong>Matrícula:</strong> {row['Matrícula']}"
            )
            
            #Personalizamos el mapa.
            folium.Marker(
                location=[row['Latitud'], row['Longitud']],
                popup=folium.Popup(popup_text, max_width=300),
                icon=folium.Icon(color='green')
            ).add_to(map_ba)
            
    #Se llama al mapa por si la interfaz de desarrollo incluye un visualizador.
    map_ba
    
    #Se guarda el mapa con el archivo y dirección introducidas en el llamado de la función.
    map_ba.save(nombre_archivo, direccion)
    
    #Se llama al mapa abriéndolo en el navegador para los casos donde el interfaz no tenga visualizador.
    webbrowser.open(nombre_archivo)
                    
    return map_ba

#%% Funciones de filtrado de datos por circunferencias o polígonos.

#Calcula la distancia entre dos puntos de una esfera(la tierra) a través de la fórmula de Haversine.
def calcular_distancia(lat1, lon1, lat2, lon2):

    R = 6371.0
    
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distancia = R * c  
    
    return distancia

# Filtra los puntos fuera de la circunferencia deseada.
def filtrar_fuera_del_circulo(df, centro_lat, centro_lon, radio_km):
    
    #Limpia las filas con datos nulos en la latitud y longitud.
    df = df.dropna(subset=['Latitud', 'Longitud']).copy()
    
    #Le aplicamos la función calcular distancia a todos las filas y se la aplicamos a la nueva columna "distancia".
    df['Distancia'] = df.apply(lambda row: calcular_distancia(
        centro_lat, centro_lon, row['Latitud'], row['Longitud']), axis=1)
    
    #Con la nueva columna calculamos los que se encuentran a más distancia de la deseada.
    fuera_del_circulo = df[df['Distancia'] > radio_km].copy()
    
    #Devolvemos los valores por fuera de la circunferencia.
    return fuera_del_circulo

#Crea un objeto Path con la lista de coordenadas dadas.
def crear_poligono(coordenadas):
    poligono_path = Path([(lon, lat) for lat, lon in coordenadas])
    return poligono_path

#Utilizamos las funciones de un objeto Path para obtener los datos por fuera de este polígono.
def filtrar_fuera(df, poligono):
    puntos_fuera = df[~df.apply(lambda row: poligono.contains_point((row['Longitud'], row['Latitud'])), axis=1)]
    return puntos_fuera

#Utilizamos las funciones de un objeto Path para obtener los datos que pertenecen al polígono.
def filtrar_dentro(df, poligono):
    puntos_dentro = df[df.apply(lambda row: poligono.contains_point((row['Longitud'], row['Latitud'])), axis=1)]
    return puntos_dentro

