# Data

## The data for this assignment was selected to analyze EV charging infrastructure in North Carolina.

1. chargers.geojson\
This data set provides all registered public electric charging stations in North Carolina. It provides more qualitative information like the name of the station or general directions to the station, along with the necessary coordinates to map the stations.\
**Source:** https://afdc.energy.gov/data_download

2. counties.geojson\
This dataset contains the county boundaries for North Carolina.\
**Source:** https://gis11.services.ncdot.gov/arcgis/rest/services/NCDOT_CountyBdy_Poly/MapServer/0

3. roads.geojson\
This dataset contains all of the existing major roads in North Carolina. The original source data was a geodatabase, so I converted it to a GeoJSON in QGIS. While doing so, I selected only interstates and US routes so that the data was not so bulky with every single minor NC road. Now, the analysis can focus chargers accessible by major highways and roads.\
**Source:**  https://connect.ncdot.gov/resources/gis/Pages/GIS-Data-Layers.aspx

5. unc_parking.geojson\
This dataset includes geometries for each of the parking structures on UNC's campus.\
**Source:** https://go.unc.edu/i3F8P

4. evs.csv\
This dataset contains all registered cars in North Carolina counties by type. In particular, I will be interested in pulling the number of electric vehicles in each county.\
**Source:** https://www.ncdot.gov/initiatives-policies/environmental/climate-change/Pages/zev-registration-data.aspx
