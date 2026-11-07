
# importing modules
print("Importing modules")
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages 
import argparse


parser = argparse.ArgumentParser(
        description="A program that makes an Atlas of permitted composting locations."
    )
parser.add_argument("statefp", help="The STATEFP code: for example, North Carolina is '37'")
parser.add_argument("statename", help="The STATE_NAME code to be printed on the Atlas")
parser.add_argument(
        "--facecolor", default="limegreen",
        help="Color of selected county"
    )
parser.add_argument(
        "--pdfname", default = "state_compost_map.pdf",
        help="Name of exported Atlas pdf"
)
args = parser.parse_args()
statefp = args.statefp
statename = args.statename
county_facecolor = args.facecolor
pdfname = args.pdfname


# getting the US census data
print("Loading census data")
url_0 = "https://www2.census.gov/geo/tiger/GENZ2024/shp/" # url for census tiger data 
url_county = "cb_2024_us_county_500k.zip" # county level
url_state = "cb_2024_us_state_500k.zip" # state level 


## code for county level data 
print("Selecting state")
counties = gpd.read_file(url_0+url_county)
state_counties = counties.loc[counties["STATEFP"] == statefp].copy()
state_counties = counties.loc[counties["STATE_NAME"] == statename].copy()
state_counties = state_counties.sort_values("NAME").reset_index(drop=True)


# ## Spatial Join


# Read data
print("Loading compost")
compost = gpd.read_file("data/compost_locations.geojson")
compost = compost.to_crs(epsg=4269)
compost = compost[["Name","geometry"]].copy()

# spatial join
print("Completing spatial join")
compost_by_county = gpd.sjoin(compost, state_counties, predicate='within')


# compost count in each county

compost_count = compost_by_county["NAME"].value_counts()


# creating new table

compost_count_table = compost_count.reset_index()
compost_count_table.columns = ["NAME", "Compost"]


# add new column
print("Cleaning data")
compost_by_county = state_counties.merge(compost_count_table, on="NAME", how="left")
compost_by_county["Compost"] = compost_by_county["Compost"].fillna(0)
compost_by_county["Compost"] = compost_by_county["Compost"].astype(int)

# filtering for only needed columns

compost_by_county = compost_by_county[["NAME", "geometry", "Compost"]].copy()


# ## Atlas 


# function with county and ax being the parameter
print("Making map functions")
def county_map(county, ax):
    selected = compost_by_county[compost_by_county["NAME"] == county]
    selected.plot(ax=ax, edgecolor="black", facecolor=county_facecolor)
    ax.set_axis_off()


def locator_map(county, ax):
    selected = compost_by_county[compost_by_county["NAME"] == county]
    compost_by_county.plot(ax=ax, edgecolor="gray", facecolor="white")
    selected.plot(ax=ax, edgecolor="black", facecolor=county_facecolor)
    ax.set_axis_off()


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
        statename + " / Permitted Compost Facility Atlas",
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


print("Creating pdf")
with PdfPages(pdfname) as pdf:  
    for county in compost_by_county["NAME"]:
        county_figure(county, pdf)

print("Done!")