import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import logging

logger = logging.getLogger(__name__)

def generate_map(latitude, longitude, wind_speed, direction):
    try:
        dt = 1  
        f = 0.00012  
        wind_speed_m = wind_speed * 0.514  
        u = wind_speed_m * np.cos(np.radians(direction))  
        v = wind_speed_m * np.sin(np.radians(direction))  

        latitudes = [latitude]
        longitudes = [longitude]
        Earth_radius_in_km = 6371

        m = Basemap(projection='merc', llcrnrlat=-60, urcrnrlat=60,
                    llcrnrlon=-180, urcrnrlon=180, resolution='i')

        for _ in range(100):  
            new_lon = longitudes[-1] + (u * dt * 360) / (2 * np.pi * Earth_radius_in_km * np.cos(np.radians(latitudes[-1])))
            new_lat = latitudes[-1] + (v * dt * 360) / (2 * np.pi * Earth_radius_in_km)
            new_lat += (f * dt * u) / (2 * np.pi * Earth_radius_in_km)

            new_lon = np.clip(new_lon, -180, 180)
            new_lat = np.clip(new_lat, -90, 90)

            x, y = m(new_lon, new_lat)

            if m.is_land(x, y):
                longitudes.append(new_lon)
                latitudes.append(new_lat)
                break
            else:
                longitudes.append(new_lon)
                latitudes.append(new_lat)

        plt.clf()
        fig, ax = plt.subplots(figsize=(10, 7))
        
        m = Basemap(projection='merc', llcrnrlat=min(latitudes) - 5, urcrnrlat=max(latitudes) + 5,
                    llcrnrlon=min(longitudes) - 5, urcrnrlon=max(longitudes) + 5, resolution='i')

        m.drawcoastlines(linewidth=0.5)
        m.drawcountries(linewidth=0.5)
        m.fillcontinents(color='lightgreen', lake_color='aqua')
        m.drawmapboundary(fill_color='aqua')
        m.drawrivers(color='blue')
        m.drawparallels(np.arange(-90., 91., 5.), labels=[1, 0, 0, 0], linewidth=0.5, color='grey', dashes=[1, 2])
        m.drawmeridians(np.arange(-180., 181., 5.), labels=[0, 0, 0, 1], linewidth=0.5, color='grey', dashes=[1, 2])

        x, y = m(longitudes, latitudes)
        m.plot(x, y, marker='o', color='red', markersize=5, linewidth=2, label='Cyclone Track')

        landfall_x, landfall_y = m(longitudes[-1], latitudes[-1])
        m.plot(landfall_x, landfall_y, marker='x', color='black', markersize=10, label='Landfall Point')

        plt.xlabel('Longitude', fontsize=12)
        plt.ylabel('Latitude', fontsize=12)
        plt.title('Cyclone Trajectory and Landfall Prediction', fontsize=15)
        plt.legend(loc='upper right')

        image_directory = 'trajectories'
        os.makedirs(image_directory, exist_ok=True)

        image_filename = 'cyclone_trajectory.png'
        image_path = os.path.join(image_directory, image_filename)

        plt.savefig(image_path)
        plt.close('all')

        return image_path

    except Exception as e:
        logger.error(f"Error in generate_map: {str(e)}")
        raise