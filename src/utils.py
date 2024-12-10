import pandas as pd
import geopandas as gpd
from shapely import wkt
from shapely.geometry import MultiPolygon, Polygon
import rasterio
from rasterio.features import rasterize
import rasterio.transform
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def convert_to_polygon(wkt_string):
    """Converts WKT string to a Shapely Polygon or MultiPolygon."""
    try:
        return wkt.loads(wkt_string)
    except Exception as e:
        print(f"Error parsing WKT: {e}")
        return None

def multi_to_single_poly(multipoly):
    """Converts a MultiPolygon to a single Polygon (the largest by area)."""
    if isinstance(multipoly, MultiPolygon):
        return max(multipoly.geoms, key=lambda x: x.area)
    else:
        return multipoly

def rasterize_polygon(poly, out_shape=(100, 100)):
    """Rasterizes a given Polygon to a 2D array."""
    minx, miny, maxx, maxy = poly.bounds
    transform = rasterio.transform.from_bounds(minx, miny, maxx, maxy, out_shape[1], out_shape[0])
    img = rasterize([poly], out_shape=out_shape, transform=transform)
    return img

def get_dataset(path):
    """Reads a CSV file with WKT geometries, processes polygons, and rasterizes them."""
    # Load CSV as GeoDataFrame
    polygon_df = pd.read_csv(path)

    # Apply conversion and multi-to-single polygon functions
    polygon_df['geometry'] = polygon_df['geometry'].apply(convert_to_polygon)
    polygon_df['geometry'] = polygon_df['geometry'].apply(multi_to_single_poly)

    # Rasterize the polygons and add new columns
    raster_images = polygon_df['geometry'].apply(rasterize_polygon)
    polygon_df['raster'] = raster_images
    polygon_df['raster_flat'] = raster_images.apply(lambda x: x.flatten())

    return polygon_df

def process_single_fire(sub_df):
    X = []
    y = []
    for i in range(len(sub_df) - 1):
        X.append([
            sub_df.raster_flat[i], 
            sub_df.burning_index[i], 
            sub_df.evapotranspiration_al[i], 
            sub_df.fuel_moisture_1000[i], 
            sub_df.relative_humidity_max[i], 
            sub_df.specific_humidity[i], 
            sub_df.temperature_max[i], 
            sub_df.vpd[i], 
            sub_df.wind_speed[i]
        ])
        y.append(sub_df.raster_flat[i + 1])
    return X, y

def prepare_data(df):
    all_X = []
    all_y = []
    
    for fire in list(df.FIRE_NAME.unique()):
        sub_df = df[df.FIRE_NAME == fire].reset_index(drop=True)
        X, y = process_single_fire(sub_df)
        all_X.extend(X)
        all_y.extend(y)
    
    return all_X, all_y

def scale_numerical_data(X):
    scaler = MinMaxScaler()

    raster_values = [entry[0] for entry in X]  # Extract raster values
    numerical_values = [entry[1:] for entry in X]  # Extract the numeric values

    # Apply Min-Max scaling to the numerical values
    numerical_values_reshaped = np.array(numerical_values)
    scaled_numerical_values = scaler.fit_transform(numerical_values_reshaped)

    # Reassemble the list
    scaled_X = []
    for i, raster in enumerate(raster_values):
        scaled_entry = [raster] + list(scaled_numerical_values[i])
        scaled_X.append(scaled_entry)

    return scaled_X

def expand_array_elements(data):
    """
    This function takes a list of sublists where each sublist starts with a numpy array.
    """
    for i in range(len(data)):
        # Convert the numpy array (first element) to a list and extend the sublist with its elements
        array_elements = data[i][0].tolist()  # Convert the np.array to a list
        data[i] = array_elements + data[i][1:]  # Merge
        
    return data

def expand_array_elements(data):
    """
    This function takes a list of sublists where each sublist starts with a numpy array.
    """
    for i in range(len(data)):
        # Convert the numpy array (first element) to a list and extend the sublist with its elements
        array_elements = data[i][0].tolist()  # Convert the np.array to a list
        data[i] = array_elements + data[i][1:]  # Merge
        
    return data

if __name__ == "__main__":
    path = "data/dataset.csv"
    df = get_dataset(path)
    print(df)