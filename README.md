
# Geocodificación

Geocodificación a través del uso de Here API.

Este proyecto surgió por la necesidad de localizar en un mapa las direcciones de un padrón electoral de elecciones regionales intra partidarias.
Para ello, se desarrolló el código expuesto en este repositorio. Con este proyecto logré experimentar mucho con las peticiones a APIs externas y el manejo de mapas interactivos.
Por razones de privacidad, la base de datos con la que trabajé no será puesta a disposición, pero se expondrán imágenes de ejemplo de uso.


---

# El proyecto

El principal problema que encontramos en este proyecto fue la ausencia de coordenadas en la base de datos, lo que nos llevó a realizar un trabajo de geocodificación utilizando Here API. A partir de aquí, con este enfoque, me concentré en dividir de la mejor forma la base de datos para no sobrecargar la API.

Una vez realizada la división, se comenzó con las peticiones al servidor, lo que culminó en una base de datos idéntica a la primera, pero con dos columnas nuevas de latitud y longitud que nos permitieron visualizarlas en el mapa utilizando la librería Folium.

Para realizar filtros, utilizamos Matplotlib para generar polígonos que nos permitieran filtrar datos según localizaciones específicas, haciendo más versátil la utilización del programa.

