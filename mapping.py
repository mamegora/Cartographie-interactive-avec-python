import time
from selenium import webdriver
import geopandas as gpd
import pandas as pd
import folium
import matplotlib.pyplot as plt
import plotly.express as px

data_path = r"C:\Users\mameg\OneDrive\Documents\E-14\Projet_E14\choropleth_map\Pop_Region_2.csv"
shape_path =r"C:\Users\mameg\OneDrive\Documents\E-14\Projet_E14\choropleth_map\couche\regio_s.shp"
 
df = pd.read_csv(data_path)
print(df)
 
shape= gpd.read_file(shape_path)
print(shape)

df['RES_CO_REG'] = df['RES_CO_REG'].astype(int)

shape['RES_CO_REG'] = shape['RES_CO_REG'].astype(int)

carte = shape.merge(df, on="RES_CO_REG")
 
print(carte)

# Créer la carte choroplète
m = folium.Map(location=[46.3528, -72.5459], zoom_start=6)

folium.Choropleth(
    geo_data=carte,
    name='choropleth',
    data=carte,
    columns=['RES_CO_REG', 'Annee'],
    key_on='feature.properties.RES_CO_REG',
    fill_color='OrRd',
    fill_opacity=5,
    line_opacity=0.2,
    legend_name='Population du quebec par région',
    title="Population du quebec"
).add_to(m)

for i, row in shape.iterrows():
    # Récupérer le centroid du polygone
    centroid = list(row.geometry.centroid.coords)[0]
    # Ajouter un marqueur sur le centroid
    folium.Marker(location=centroid,
                  tooltip=row['RES_CO_REG'],
                  icon=folium.Icon(color='green', icon='info-sign')
                  ).add_to(m)

# Ajout de la délimitation de la province de Québec
geojson_data = shape.to_json()
geojson_layer = folium.GeoJson(data=geojson_data,
                        style_function=lambda x: {'fillColor': 'transparent', 'color': 'blue', 'weight': 2})
geojson_layer.add_to(m)

# Ajouter la couche shapefile à la carte
folium.GeoJson(shape).add_to(m)

folium.TileLayer('openstreetmap').add_to(m)
folium.TileLayer('Stamen Toner').add_to(m)
folium.TileLayer('Stamen Watercolor').add_to(m)

# Attendre que la carte se charge
time.sleep(5)

# Configurer le pilote de navigateur
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Ouvrir le fichier HTML de la carte dans le navigateur
driver.get('file:///C:/Users/mameg/OneDrive/Documents/E-14/Projet_E14/choropleth_map/map.html')

# Attendre que la carte soit chargée
time.sleep(5)

# Prendre une capture d'écran de la carte et l'enregistrer dans un fichier PNG
driver.save_screenshot('carte_interactive.png')

# Fermer le navigateur
driver.quit()

folium.LayerControl(position='topleft').add_to(m)

folium.Marker([47.9488, -77.7787], 
               popup='<strong>Abitibi-Témiscamingue </strong>',
              tooltip=folium.Tooltip,
               ).add_to(m)

m.save('map.html')










