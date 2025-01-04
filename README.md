# Geocodificación
Geocodificación a través del uso de Here Api.

Este proyecto surgió por la necesidad de localizar en un mapa las direcciones de un padrón electoral de elecciones regionales intra partidarias.
Para ello se realizó el código expuesto en este repositorio. Con este proyecto logre experimentar mucho con las peticiones a apis externos y el manejo de mapas interactivos.
Por razones de privacidad la base de datos con la que trabaje no será puesta a disposición, pero se expondran imagenes de ejemplo de uso.

---

# El proyecto

El principal problema que nos encontramos en este proyecto fue la ausencia de coordenadas en la base de datos lo que nos llevo a realizar un trabajo de geocodificacion utilizando Here Api. Apartir de aca con este enfoque me consentre en dividir de la mejor forma la base de datos para no sobrecargar la API.

Una ves relizada la divicion se empeso con las peticiones al servidor que culmino con un base de datos identica a la primera pero con dos columnas nuevas de latitud y longitud que nos permitio visualizarlas en el mapa utilizando la libreria Folium.

Para realizar filtros utilizamos MatPlot lib para generar poligonos que nos permitirian filtrar datos segun localizaciones espesificas lo que hace mas versatil la utilizacion del programa.
