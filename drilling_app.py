# Import Libraries
import streamlit as st
import pandas as pd
import plotly_express as px
from streamlit_option_menu import option_menu
from PIL import Image

# Insert an icon
icon = Image.open("Resources/well.jpg")

# State the design of the app
st.set_page_config(page_title="Drilling App", page_icon=icon)

# Insert css codes to improve the design of the app
st.markdown(
    """
<style>
h1 {text-align: center;
}
body {background-color: #DCE3D5;
      width: 1400px;
      margin: 15px auto;
}
</style>""",
    unsafe_allow_html=True,
)

# Title of the app
st.title("Drilling Engineering App :link:")

st.write("---")

# Add information of the app
st.markdown(
    """ This app is used to visualize 3D Trajectories of directional wells, to upload csv files, 
to call data, and to realize basic calculations.

**Python Libraries:** Streamlit, pandas, plotly, PIL.
"""
)

# Add additional information
expander = st.expander("About")
expander.write("This app is very useful for drilling projects")

# Insert image
image = Image.open("Resources/dd.jpg")
st.image(image, width=100, use_column_width=True)

# Insert video
st.subheader("**Drilling Fundamentals**")
video = open("Resources/drilling.mp4", "rb")
st.video(video)

# Add caption
st.caption("Video about drilling fundamentals")

# Sidebar
Logo = Image.open("Resources/ESPOL.png")
st.sidebar.image(Logo)

# Add title to the sidebar section
st.sidebar.title(":arrow_down: **Navigation**")

# Upload files
upload_file = st.sidebar.file_uploader("Upload your csv file")

# Pages
with st.sidebar:
    options = option_menu(
        menu_title="Menu",
        options=["Home", "Data", "3D Plots", "Basic Calculations"],
        icons=["house", "tv-fill", "box", "calculator"],
    )


# Useful functions
def data(dataframe):
    st.header("**Dataframe header**")
    st.write(dataframe.head())
    st.header("**Statistical information**")
    st.write(dataframe.describe())


# Call dataframe
if upload_file:
    df = pd.read_csv(upload_file)

# Call web app sections
if options == "Data":
    data(df)

