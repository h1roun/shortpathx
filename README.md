# Algeria Router

A smart routing application for navigating across Algeria, with special focus on routes from Bejaia to other destinations.

## Features

- Interactive map visualization using Folium and OpenStreetMap data
- Smart route finding using OSMnx and NetworkX
- Beautiful UI with Bulma CSS framework
- Search for routes between any two locations in Algeria
- Quick access to popular destinations
- Distance calculation and route optimization

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

4. Open your browser and navigate to http://127.0.0.1:5000/

## Requirements

- Python 3.7+
- Flask
- OSMnx
- NetworkX
- Folium
- Geopy

## First Run Notice

On first run, the application will download the road network data for Algeria, which may take some time depending on your internet connection. This data will be cached for subsequent runs.

## Screenshots

![Algeria Router Screenshot](static/img/screenshot.png)

## License

MIT License

## Credits

- OpenStreetMap contributors for map data
- OSMnx for network analysis tools
- Bulma for the CSS framework
# shortpathx
