#!/usr/bin/env python
# coding: utf-8

# # GEOG 592 — Week 11 Homework
# ## Jupyter Notebook to Py

# ## Data Preparation and Spatial Join

# In[12]:


import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse
from matplotlib.backends.backend_pdf import PdfPages 


# In[13]:


# getting the US census data
print("Loading census data")
url_0 = "https://www2.census.gov/geo/tiger/GENZ2024/shp/" # url for census tiger data 
url_county = "cb_2024_us_county_500k.zip" # county level
url_state = "cb_2024_us_state_500k.zip" # state level 


## code for county level data 
print("Selecting North Carolina")
counties = gpd.read_file(url_0+url_county)
nc_counties = counties.loc[counties["STATEFP"] == "37"].to_crs(6543).copy()
nc_counties = nc_counties.sort_values("NAME").reset_index(drop=True)


# ## Spatial Join

# In[14]:


# Read data
print("Loading compost")
compost = gpd.read_file("data/Permitted_Compost_Facilities.geojson")
compost = compost.to_crs(epsg=6543)
compost = compost[["PermitName","geometry"]].copy()

# spatial join
print("Completing spatial join")
compost_by_county = gpd.sjoin(compost, nc_counties, predicate='within')


# In[15]:


# compost count in each county

compost_count = compost_by_county["NAME"].value_counts()


# In[16]:


# creating new table

compost_count_table = compost_count.reset_index()
compost_count_table.columns = ["NAME", "Compost"]


# In[17]:


# add new column
print("Cleaning data")
compost_by_county = nc_counties.merge(compost_count_table, on="NAME", how="left")
compost_by_county["Compost"] = compost_by_county["Compost"].fillna(0)
compost_by_county["Compost"] = compost_by_county["Compost"].astype(int)

# filtering for only needed columns

compost_by_county = compost_by_county[["NAME", "geometry", "Compost"]].copy()


# ## Atlas 

# In[18]:


# function with county and ax being the parameter
print("Making map functions")
def county_map(county, ax):
    selected = compost_by_county[compost_by_county["NAME"] == county]
    selected.plot(ax=ax, edgecolor="black", facecolor="limegreen")
    ax.set_axis_off()


def locator_map(county, ax):
    selected = compost_by_county[compost_by_county["NAME"] == county]
    compost_by_county.plot(ax=ax, edgecolor="gray", facecolor="white")
    selected.plot(ax=ax, edgecolor="black", facecolor="limegreen")
    ax.set_axis_off()


# In[19]:


# Defining number of facilities map function
def county_info(county, ax):
    selected = compost_by_county[compost_by_county["NAME"] == county]

    facilities = selected["Compost"].iloc[0]

    ax.text(
        -0.5, 0.8,
        f"Permitted Compost Facilities: {facilities}",
        transform=ax.transAxes,
        fontsize=14,
        color="black",
        va="top"
    )

    ax.set_axis_off()


# In[20]:


def county_figure(county, pdf):

    fig = plt.figure(figsize=(12, 8))

    # [left, bottom, width, height] as fractions of the figure
    ax_county = fig.add_axes([0.05, 0.23, 0.55, 0.54])
    ax_locator = fig.add_axes([0.65, 0.12, 0.30, 0.32])
    ax_info = fig.add_axes([0.85, 0.48, 0.30, 0.30])


    county_map(county, ax_county)
    locator_map(county, ax_locator)
    county_info(county, ax_info)

    # Page heading
    fig.text(
        0.05, 0.94,
        "NORTH CAROLINA / Permitted Compost Facility Atlas",
        fontsize=10,
        color="olivedrab"
    )

    fig.text(
        0.05, 0.87,
        f"{county} County",
        fontsize=28,
        fontweight="bold"
    )

    # Footer
    fig.text(
        0.05, 0.03,
        "Sources: U.S. Census Bureau, NC OneMap",
        fontsize=9,
        color="gray"
    )

    pdf.savefig(fig, dpi=50)
    plt.close(fig)


# In[21]:

print("Creating pdf")
with PdfPages("NC_Compost_Counties.pdf") as pdf:  
    for county in compost_by_county["NAME"]:
        county_figure(county, pdf)


# In[ ]:


# get_ipython().run_line_magic('pip', 'install nbconvert')
# python3 -m nbconvert --to script "lexleach-hw11-jupyter_to_py.ipynb"