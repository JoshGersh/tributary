# Tributary

Backend infrastructure for Ford's sensor streaming system. This codebase includes a Flask server that records data to a Redis database and exposes two endpoints.

## Endpoints

- **/record**: Periodically called by embedded sensors within a vehicle to post data to the database.
- **/collect**: Used by a user-facing mobile application to retrieve data from the database.

## Overview

The Tributary project is designed to handle sensor data streaming for Ford vehicles. It ensures efficient data recording and retrieval through a robust backend infrastructure.

## Technologies Used

- **Flask**: For creating the server.
- **Redis**: For data storage.

## Usage

1. **/record**: Sensors post data to this endpoint.
2. **/collect**: Mobile applications retrieve data from this endpoint.

## License

This project is open-source and available under the MIT License.
