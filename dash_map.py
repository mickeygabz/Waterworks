# import libraries
import streamlit as st
import pandas as pd
import folium as fl
from streamlit_folium import st_folium
import pandas as pd
import geopandas as gpd
from branca.element import Template, MacroElement

# Clear streamlit cache code to run on cmd
# streamlit cache clear


# References
"""
- popup: https://towardsdatascience.com/use-html-in-folium-maps-a-comprehensive-guide-for-data-scientists-3af10baf9190
- Legend: https://nbviewer.org/gist/talbertc-usgs/18f8901fc98f109f2b71156cf3ac81cd

- Icons: https://getbootstrap.com/docs/3.3/components/#glyphicons-glyphs
"""
"""
May the ghosts of braincells that unalived themselves while working on this code guide you
and may the tears shed provide you with comfort that you can do it.
"""


# Legend template
template = """

{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>jQuery UI Draggable - Default functionality</title>
	<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

	<script src="https://code.jquery.com/jquery-1.12.4.js"></script>
	<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
	
	<script>
	$( function() {
		$( "#maplegend" ).draggable({
										start: function (event, ui) {
												$(this).css({
														right: "auto",
														top: "auto",
														bottom: "auto"
												});
										}
								});
});

	</script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
		style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
		 border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
		 
<div class='legend-title'>Overall Compliance Legend</div>
<div class='legend-scale'>
	<ul class='legend-labels'>
		<li><span style='background:red;opacity:0.7;'></span>Unacceptable <50%</li>
		<li><span style='background:#FFA62F;opacity:0.7;'></span>Tolerable 50%-70%</li>
		<li><span style='background:#4AA02C;opacity:0.7;'></span>Acceptable 70%-90%</li>
		<li><span style='background:#3BB9FF;opacity:0.7;'></span>Ideal >90%</li>

	</ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
	.maplegend .legend-title {
		text-align: left;
		margin-bottom: 5px;
		font-weight: bold;
		font-size: 90%;
		}
	.maplegend .legend-scale ul {
		margin: 0;
		margin-bottom: 5px;
		padding: 0;
		float: left;
		list-style: none;
		}
	.maplegend .legend-scale ul li {
		font-size: 80%;
		list-style: none;
		margin-left: 0;
		line-height: 18px;
		margin-bottom: 2px;
		}
	.maplegend ul.legend-labels li span {
		display: block;
		float: left;
		height: 16px;
		width: 30px;
		margin-right: 5px;
		margin-left: 0;
		border: 1px solid #999;
		}
	.maplegend .legend-source {
		font-size: 80%;
		color: #777;
		clear: both;
		}
	.maplegend a {
		color: #777;
		}
</style>
{% endmacro %}"""

# Popup function
def popup_html(df):
    try:
        site_description = df["sample_pt_desc"]

        html = (
            """<!DOCTYPE html>

	<center><h5 style="margin-bottom:5"; width="200px">{}</h4>""".format(
                site_description
            )
            + """</center>

	</html>
	"""
        )
        return html
    except KeyError:
        site_description = df["treatment_works"]

        html = (
            """<!DOCTYPE html>

	<center><h5 style="margin-bottom:5"; width="200px">{}</h4>""".format(
                site_description
            )
            + """</center>

	</html>
	"""
        )
        return html


# Compliance color chooser function
def compliance_color(row):
    if row["overall_compliance_percentage"] < 50:
        return "red"
    elif row["overall_compliance_percentage"] < 70:
        return "orange"
    elif row["overall_compliance_percentage"] < 90:
        return "green"
    elif row["overall_compliance_percentage"] > 89:
        return "blue"


# Year and quarter selection function
def display_time_filters(df):
    year_list = list(df["year"].unique())
    year_list.sort()
    year = st.sidebar.selectbox("Year", year_list, len(year_list) - 1)
    quarter = st.sidebar.radio("Quarter", ["Jan-Mar", "Apr-Jun", "Jul-Sep", "Oct-Dec"])
    st.header(f"{year} {quarter}")
    return year, quarter


# Site selection function
def display_site_filter(df, site_name):
    site_list = [""] + list(df["sample_pt_desc"].unique())
    site_list.sort()
    site_index = (
        site_list.index(site_name) if site_name and site_name in site_list else 0
    )
    return st.sidebar.selectbox("Select Site", site_list, site_index)


# Parameter selection function
def display_param_filter():
    param_list = [""] + [
        "Chemical Oxygen Demand",
        "Conductivity",
        "E.coli",
        "Nitrate (NO3 as N)",
        "pH",
        "Phosphate (PO4 as P)",
    ]
    # ["cod", "conductivity", "e_coli", "nitrate", "pH", "phosphate"]
    param_list.sort()
    return st.sidebar.selectbox("Filter by Parameter", param_list)


# Parameter thresholds function
def param_filter(param):
    if param == "E.coli":
        return 0, 400, "e_coli"
    elif param == "Chemical Oxygen Demand":
        return 0, 30, "cod"
    elif param == "Conductivity":
        return 0, 70, "conductivity"
    elif param == "Nitrate (NO3 as N)":
        return 0, 6, "nitrate"
    elif param == "pH":
        return 6, 9, "pH"
    elif param == "Phosphate (PO4 as P)":
        return 0, 0.05, "phosphate"


# Get test site compliances function
def display_compliance_test_site(
    df, year, quarter, site_name, column, string_format="${:,}", is_median=False
):
    df = df[(df["year"] == year) & (df["quarter"] == quarter)]
    if site_name:
        df = df[df["sample_pt_desc"] == site_name]
    df.drop_duplicates(inplace=True)

    st.metric(column[1], f"{round(df[column[0]].mean(),2)}%")


# Get wwtp compliances function
def display_compliance_wwtp(
    df, site_name, column, string_format="${:,}", is_median=False
):
    if site_name:
        df = df[df["treatment_works"] == site_name[0]]
    df.drop_duplicates(inplace=True)

    st.metric(column[1], df[column[0]].item())


# Map creation function
def map(df, df2, only1, only2, only3, only4, only5):
    vaal_map = fl.Map(
        location=[-26.3584, 28.17648],
        zoom_start=8.5,
        scrollWheelZoom=False,
        tiles="Stamen Terrain",
    )

    river = fl.FeatureGroup(name="River")
    river.add_child(
        fl.GeoJson(
            data=only1["geometry"],
            name="Streams",
            style_function=lambda x: {"weight": 1},
        )
    )
    river.add_child(
        fl.GeoJson(
            data=only2["geometry"],
            name="Tributaries",
            style_function=lambda x: {"weight": 1},
        )
    )
    river.add_child(
        fl.GeoJson(
            data=only3["geometry"],
            name="River branches",
            style_function=lambda x: {"weight": 2},
        )
    )
    river.add_child(
        fl.GeoJson(
            data=only4["geometry"],
            name="Main river",
            style_function=lambda x: {"weight": 3},
        )
    )
    river.add_child(
        fl.GeoJson(
            data=only5["geometry"],
            name="Main river",
            style_function=lambda x: {"weight": 3},
        )
    )
    vaal_map.add_child(river)

    # Test sites
    vaal = fl.FeatureGroup(name="Vaal")

    for _, site in df.iterrows():
        vaal.add_child(
            fl.Marker(
                location=[site["latitude"], site["longitude"]],
                popup=fl.Popup(fl.Html(popup_html(site), script=True), max_width=500),
                tooltip=site["sample_pt_desc"],
                icon=fl.Icon(
                    color=compliance_color(site),
                    icon="glyphicon glyphicon-tint",
                ),
            )
        )
    vaal_map.add_child(vaal)

    # WWTP sites
    wwtp = fl.FeatureGroup(name="WWTP")

    for _, site in df2.iterrows():
        wwtp.add_child(
            fl.Marker(
                location=[site["lat"], site["long"]],
                popup=fl.Popup(fl.Html(popup_html(site), script=True), max_width=500),
                tooltip=site["treatment_works"],
                icon=fl.Icon(
                    color="white", icon="fa-industry", prefix="fa", icon_color="black"
                ),
            )
        )
    vaal_map.add_child(wwtp)

    macro = MacroElement()
    macro._template = Template(template)

    vaal_map.get_root().add_child(macro)

    fl.LayerControl().add_to(vaal_map)

    st_map = st_folium(vaal_map, width=700, height=450)
    # Don't change this code unless you want to have a bad time or you have a better WORKING method
    site_name = ""
    try:
        if st_map["last_active_drawing"]:
            coordinates = st_map["last_active_drawing"]["geometry"]["coordinates"]
            site_name = df["sample_pt_desc"][
                (df["latitude"] == coordinates[1]) & (df["longitude"] == coordinates[0])
            ].item()
        return site_name
    except ValueError:
        if st_map["last_active_drawing"]:
            coordinates = st_map["last_active_drawing"]["geometry"]["coordinates"]
            site_name = list(
                df2["treatment_works"][
                    (df2["lat"] == coordinates[1]) & (df2["long"] == coordinates[0])
                ]
            )

        return site_name


# Map display function
def display_map(df, df2, year, quarter, param, only1, only2, only3, only4, only5):
    if param == "":
        df = df[(df["year"] == year) & (df["quarter"] == quarter)]

        return map(df, df2, only1, only2, only3, only4, only5)
    else:
        low_end, high_end, actual = param_filter(param)
        df = df[
            (df["year"] == year)
            & (df["quarter"] == quarter)
            & ((df[actual] < low_end) | (df[actual] > high_end))
        ]

        return map(df, df2, only1, only2, only3, only4, only5)


# Load data from databricks function
@st.cache(suppress_st_warning=True)

def main():

    # Load data
    wwtp_df = pd.read_csv('data/wwtp.csv')
    test_sites_df = pd.read_csv('data/merged.csv')
    only1 = gpd.read_file("data/river/only1.shp")
    only2 = gpd.read_file("data/river/only2.shp")
    only3 = gpd.read_file("data/river/only3.shp")
    only4 = gpd.read_file("data/river/only4.shp")
    only5 = gpd.read_file("data/river/only5.shp")

    # Display Filters and Map
    year, quarter = display_time_filters(test_sites_df)
    param = display_param_filter()
    site_name = display_map(
        test_sites_df, wwtp_df, year, quarter, param, only1, only2, only3, only4, only5
    )
    if site_name in list(test_sites_df["sample_pt_desc"]) or site_name == "":
        site_name = display_site_filter(test_sites_df, site_name)

    # Display Metrics
    if type(site_name) == list:
        st.subheader(f"{site_name[0]} Compliance")
    else:
        st.subheader(f"{site_name} Compliance")

    # test site col titles
    phys = ["physical_compliance_percentage", "Physical"]
    chem = ["chemical_compliance_percentage", "Chemical"]
    bact = ["bacteriological_compliance_percentage", "Bacteriological"]
    bio = ["biological_compliance_percentage", "Biological"]
    overall = ["overall_compliance_percentage", "Overall"]

    # wwtp col titles
    p_class = ["plant_class", "Plant Class"]
    discharge = ["river_discharge", "River Discharge"]
    amnt = ["discharge_amount_kl_per_day", "Discharge Amount(kl/day)"]
    tests = ["tests", "No of Tests"]
    fail = ["failures", "No of Failures"]

    if site_name in list(test_sites_df["sample_pt_desc"]) or site_name == "":
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            display_compliance_test_site(
                df=test_sites_df,
                year=year,
                quarter=quarter,
                site_name=site_name,
                column=phys,
            )
        with col2:
            display_compliance_test_site(
                df=test_sites_df,
                year=year,
                quarter=quarter,
                site_name=site_name,
                column=chem,
            )
        with col3:
            display_compliance_test_site(
                df=test_sites_df,
                year=year,
                quarter=quarter,
                site_name=site_name,
                column=bact,
            )
        with col4:
            display_compliance_test_site(
                df=test_sites_df,
                year=year,
                quarter=quarter,
                site_name=site_name,
                column=bio,
            )
        with col5:
            display_compliance_test_site(
                df=test_sites_df,
                year=year,
                quarter=quarter,
                site_name=site_name,
                column=overall,
            )
    else:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            display_compliance_wwtp(
                df=wwtp_df,
                site_name=site_name,
                column=p_class,
            )
        with col2:
            display_compliance_wwtp(
                df=wwtp_df,
                site_name=site_name,
                column=discharge,
            )
        with col3:
            display_compliance_wwtp(
                df=wwtp_df,
                site_name=site_name,
                column=amnt,
            )
        cpad1, col4, col5, pad2 = st.columns(([1, 1, 1, 1]))
        with col4:
            display_compliance_wwtp(
                df=wwtp_df,
                site_name=site_name,
                column=tests,
            )
        with col5:
            display_compliance_wwtp(
                df=wwtp_df,
                site_name=site_name,
                column=fail,
            )


if __name__ == "__main__":
    main()
