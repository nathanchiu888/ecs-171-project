import React, { useState } from 'react';
import { MapContainer, TileLayer, Polygon, Popup } from 'react-leaflet';
import './MapComponent.css';

const MapComponent = () => {
  const [coords, setCoords] = useState([]);
  const [predictedCoords, setPredictedCoords] = useState([]);
  const [formData, setFormData] = useState({
    YYYYMMDD: '',
    geometry: '',
    FIRE_NAME: '',
    latitude: '',
    longitude: '',
    burning_index: '',
    evapotranspiration_al: '',
    fuel_moisture_1000: '',
    relative_humidity_max: '',
    specific_humidity: '',
    temperature_max: '',
    vpd: '',
    wind_speed: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleAddCoordinate = (e) => {
    e.preventDefault();

    const geometryPoints = formData.geometry
      .replace('POLYGON ((', '') // Remove "POLYGON (("
      .replace('))', '') // Remove "))"
      .split(', ')
      .map((point) => {
        const [lng, lat] = point.split(' ').map(Number);
        return { lat, lng };
      });

    const newCoord = {
      ...formData,
      geometry: geometryPoints,
    };

    setCoords((prevCoords) => [...prevCoords, newCoord]);

    // Send the data to the Flask backend
    sendToFlaskBackend([newCoord]);

    setFormData({
      YYYYMMDD: '',
      geometry: '',
      FIRE_NAME: '',
      latitude: '',
      longitude: '',
      burning_index: '',
      evapotranspiration_al: '',
      fuel_moisture_1000: '',
      relative_humidity_max: '',
      specific_humidity: '',
      temperature_max: '',
      vpd: '',
      wind_speed: '',
    });
  };

  const sendToFlaskBackend = async (data) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ inputs: data }),
      });

      const result = await response.json();

      // Use the response to update predictedCoords
      if (result.polygons) {
        const predictedPolygons = result.polygons.map((polygonWKT) => {
          const points = polygonWKT
            .replace('POLYGON ((', '')
            .replace('))', '')
            .split(', ')
            .map((point) => {
              const [lng, lat] = point.split(' ').map(Number);
              return { lat, lng };
            });

          return { geometry: points, FIRE_NAME: 'Predicted' };
        });

        setPredictedCoords((prevPredictedCoords) => [
          ...prevPredictedCoords,
          ...predictedPolygons,
        ]);
      }
    } catch (error) {
      console.error('Error sending data to Flask backend:', error);
    }
  };

  return (
    <div>
      <h2>Enter Wildfire Data</h2>

      <form onSubmit={handleAddCoordinate} className="form-container">
        {Object.keys(formData).map((field) => (
          <div className="form-group" key={field}>
            <label htmlFor={field}>
              {field.replace(/_/g, ' ')}:
            </label>
            {field === 'geometry' ? (
              <textarea
                id={field}
                name={field}
                value={formData[field]}
                onChange={handleChange}
                required
              />
            ) : (
              <input
                type="text"
                id={field}
                name={field}
                value={formData[field]}
                onChange={handleChange}
                required
              />
            )}
          </div>
        ))}
        <button type="submit">Add Coordinate</button>
      </form>

      <MapContainer center={[37.5, -119.5]} zoom={6} style={{ height: '500px', width: '100%' }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

        {coords.map((coord, index) => (
          <Polygon
            key={`blue-${index}`}
            positions={coord.geometry}
            pathOptions={{ color: 'blue', fillColor: 'blue', fillOpacity: 0.3 }}
          >
            <Popup>
              <b>{coord.FIRE_NAME}</b> <br />
              Date: {coord.YYYYMMDD} <br />
              Temperature Max: {coord.temperature_max} °C <br />
              Wind Speed: {coord.wind_speed} km/h
            </Popup>
          </Polygon>
        ))}

        {predictedCoords.map((coord, index) => (
          <Polygon
            key={`red-${index}`}
            positions={coord.geometry}
            pathOptions={{ color: 'red', fillColor: 'red', fillOpacity: 0.3 }}
          >
            <Popup>
              <b>{coord.FIRE_NAME} (Prediction)</b>
            </Popup>
          </Polygon>
        ))}
      </MapContainer>
    </div>
  );
};

export default MapComponent;
