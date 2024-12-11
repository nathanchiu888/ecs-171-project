# FireSight - Wildfire Prediction Tool

*ML Project for ECS 171 Class @ UC Davis*

FireSight is a wildfire prediction tool that leverages Convolutional Neural Networks (CNNs) and Long Short-Term Memory networks (LSTMs) to predict the next timesteps of wildfires based on climate data and initial fire coordinates. This tool allows users to input critical climate conditions and view predicted fire spread, providing valuable insights for wildfire management and preparedness.

## Features
- **Web Application**: A user-friendly interface to input the initial coordinates of a wildfire and relevant climate data.
- **Predictive Modeling**: Uses CNNs and LSTMs to predict the next timestep of wildfire spread.
- **Climate Conditions**: Supports the following inputs:
  - **Burning Index**
  - **Evapotranspiration**
  - **Fuel Moisture across 1000hrs**
  - **Relative Humidity**
  - **Specific Humidity**
  - **Temperature**
  - **Vapor Pressure Deficit**
  - **Wind Speed**

## Why LSTMs and CNNs?
We chose to use **LSTMs** and **CNNs** to address the complexities of wildfire prediction. Here's why:

- **LSTMs (Long Short-Term Memory networks)**: LSTMs are excellent for capturing temporal dependencies in data. This is crucial for wildfire prediction because wildfires evolve over time, and LSTMs can model these sequential changes, allowing the system to remember and utilize past information when making predictions about the future.

- **CNNs (Convolutional Neural Networks)**: While LSTMs are great at understanding time-based data, we found that they struggle with spatial information, which is key for predicting wildfire spread. CNNs, on the other hand, excel at extracting spatial features from data, making them ideal for understanding the spatial dynamics of fire spread. By combining CNNs with LSTMs, we ensure that both temporal and spatial dependencies are effectively modeled.

Through our testing, we realized that the addition of CNNs significantly improved the model's ability to understand spatial relationships in wildfire behavior, leading to more accurate predictions.

## Team Members
Nathan Chiu, Ashton Lee, Jessie Lin, Suyash Goel, Anvi Kalucha

## Getting Started

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/nathanchiu888/ecs-171-project.git
   cd ecs-171-project
   ```
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
