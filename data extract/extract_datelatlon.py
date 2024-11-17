import geopandas as gpd
import os
import pandas as pd

directory = os.path.expanduser('~/Desktop/California_spread_2012_2021')

# init list to store the extracted data
extracted_data = []

for filename in os.listdir(directory):
    if filename.endswith('.shp'): 
        file_path = os.path.join(directory, filename)
        
        try:
            gdf = gpd.read_file(file_path)
            #print(f"Columns in {filename}: {gdf.columns.tolist()}")
            
            # Check the geometry type and extract coordinates
            for index, row in gdf.iterrows():
                if row['geometry'].geom_type == 'Point':
                    lat, lon = row['geometry'].y, row['geometry'].x
                elif row['geometry'].geom_type in ['Polygon', 'MultiPolygon']:
                    lat, lon = row['geometry'].centroid.y, row['geometry'].centroid.x
                else:
                    continue  # Skip other geometries
                
                # Check for available date columns
                if 'ACQ_DATE' in row:
                    date_value = row['ACQ_DATE']
                elif 'YYYYMMDD' in row:
                    date_value = row['YYYYMMDD']
                else:
                    date_value = None  # No date information

                # Extract fire name
                fire_name = row.get('SATELLITE', None)  

                extracted_data.append({
                    'date': date_value,
                    'latitude': lat,
                    'longitude': lon,
                    'fire name': fire_name  
                })
        except Exception as e:
            print(f"Error processing {filename}: {e}")


# Convert the extracted data to a DataFrame for easier manipulation
extracted_df = pd.DataFrame(extracted_data)

# Convert the 'date' column to datetime format
extracted_df['date'] = pd.to_datetime(extracted_df['date'], errors='coerce')

# Sort the DataFrame by date from old to new
extracted_df = extracted_df.sort_values(by='date')

# Reset the index after sorting
extracted_df.reset_index(drop=True, inplace=True)


print(extracted_df.head()) #display few rows

# Optionally, save the sorted data to a new CSV file
extracted_df.to_csv('date_lat_lon_firename.csv', index=False)