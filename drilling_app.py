# Import Libraries
import streamlit as st
import pandas as pd
import plotly_express as px
from streamlit_option_menu import option_menu
from PIL import Image
from collections import namedtuple
from math import radians, acos, asin, cos, sin, atan, degrees, sqrt

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


def plot(dataframe):
    st.header("**Well Trajectory 3D**")
    x = st.selectbox("Enter dispns", options=dataframe.columns)
    y = st.selectbox("Enter dispew", options=dataframe.columns)
    z = st.selectbox("Enter tvd", options=dataframe.columns)
    fig = px.line_3d(dataframe, x, y, z)
    st.plotly_chart(fig)


# Useful functions for directional trajectories
# Function to calculate J well parameters

Data = namedtuple("Input", "TVD KOP BUR DH")
Output = namedtuple("Output", "R Theta TVD_EOB Md_EOB Dh_EOB Tan_len Md_total")


def well_J(data: Data, unit="ingles") -> Output:
    # Call input values
    tvd = data.TVD
    kop = data.KOP
    bur = data.BUR
    dh = data.DH
    if unit == "ingles":
        R = 5729.58 / bur
    else:
        R = 1718.87 / bur
    if dh > R:
        dc = dh - R
    elif dh < R:
        dc = R - dh
    do = tvd - kop
    doc = degrees(atan(dc / do))
    oc = sqrt(dc**2 + do**2)
    boc = degrees(acos(R / oc))
    if R < dh:
        bod = boc - doc
    elif R > dh:
        bod = boc + doc
    theta = 90 - bod
    tvd_eob = kop + abs(R * sin(radians(theta)))
    if unit == "ingles":
        md_eob = kop + (theta / bur) * 100
    else:
        md_eob = kop + (theta / bur) * 30
    dh_eob = R - R * cos(radians(theta))
    tan_len = sqrt(oc**2 - R**2)
    if unit == "ingles":
        md_total = kop + (theta / bur) * 100 + tan_len
    else:
        md_total = kop + (theta / bur) * 30 + tan_len
    output = Output(
        R=R,
        Theta=theta,
        TVD_EOB=tvd_eob,
        Md_EOB=md_eob,
        Dh_EOB=dh_eob,
        Tan_len=tan_len,
        Md_total=md_total,
    )
    names = ["R", "theta", "tvd_EOB", "MD_EOB", "DH_EOB", "Length_tan", "MD_Total"]
    for param, value in zip(names, output):
        if unit == "ingles":
            if param == "theta":
                st.success(f"{param} -> {value:.3f} degrees")
            else:
                st.success(f"{param} -> {value:.3f} ft")
        else:
            if param == "theta":
                st.success(f"{param} -> {value:.3f} degrees")
            else:
                st.success(f"{param} -> {value:.3f} m")


# Function to calculate parameters from a S-Type well
Data_S = namedtuple("Input", "TVD KOP BUR DOR DH")
Output_S = namedtuple(
    "Output", "R1 R2 Theta TVD_EOB Md_EOB Dh_EOB Tan_len Md_SOD TVD_SOD Dh_SOD Md_total"
)


def well_S(data: Data_S, unit="ingles"):
    tvd = data.TVD
    kop = data.KOP
    bur = data.BUR
    dor = data.DOR
    dh = data.DH
    if unit == "ingles":
        R1 = 5729.58 / bur
        R2 = 5729.58 / dor
    else:
        R1 = 1718.87 / bur
        R2 = 1718.87 / dor
    if dh > (R1 + R2):
        fe = dh - (R1 + R2)
    elif dh < (R1 + R2):
        fe = R1 - (dh - R2)
    eo = tvd - kop
    foe = degrees(atan(fe / eo))
    of = sqrt(fe**2 + eo**2)
    fg = R1 + R2
    fog = degrees(asin(fg / of))
    theta = fog - foe
    tvd_eob = kop + R1 * sin(radians(theta))
    if unit == "ingles":
        md_eob = kop + (theta / bur) * 100
    else:
        md_eob = kop + (theta / bur) * 30
    dh_eob = R1 - abs(R1 * cos(radians(theta)))
    tan_len = sqrt(of**2 - fg**2)
    if unit == "ingles":
        md_sod = kop + (theta / bur) * 100 + tan_len
    else:
        md_sod = kop + (theta / bur) * 30 + tan_len
    tvd_sod = tvd_eob + tan_len * abs(cos(radians(theta)))
    dh_sod = dh_eob + abs(tan_len * sin(radians(theta)))
    if unit == "ingles":
        md_total = kop + (theta / bur) * 100 + tan_len + (theta / dor) * 100
    else:
        md_total = kop + (theta / bur) * 30 + tan_len + (theta / dor) * 30

    output_S = Output_S(
        R1=R1,
        R2=R2,
        Theta=theta,
        TVD_EOB=tvd_eob,
        Md_EOB=md_eob,
        Dh_EOB=dh_eob,
        Tan_len=tan_len,
        Md_SOD=md_sod,
        TVD_SOD=tvd_sod,
        Dh_SOD=dh_sod,
        Md_total=md_total,
    )

    names = [
        "R1",
        "R2",
        "theta",
        "tvd_EOB",
        "Md_EOB",
        "Dh_EOB",
        "Lengh_tan",
        "Md_SOD",
        "tvd_SOD",
        "Dh_SOD",
        "Md_Total",
    ]
    for param, value in zip(names, output_S):
        if unit == "ingles":
            if param == "theta":
                st.success(f"{param} -> {value:.3f} degrees")
            else:
                st.success(f"{param} -> {value:.3f} ft")
        else:
            if param == "theta":
                st.success(f"{param} -> {value:.3f} degrees")
            else:
                st.success(f"{param} -> {value:.3f} m")

Data_H = namedtuple("Input", "TVD KOP BUR1 BUR2 DH")
Output_H = namedtuple(
    "Output", "R1 R2 Theta TVD_EOB1 Md_EOB1 Dh_EOB1 Tan_len Md_SOB2  Md_total"
)
def well_H(data:Data_H, unit='ingles'):
    tvd = data.TVD
    kop = data.KOP
    bur = data.BUR1
    dor = data.BUR2
    dh = data.DH
    if unit == 'ingles':
        R1 = 5729.58 / bur
        R2 = 5729.58 / dor
    else:
        R1 = 1718.87 / bur
        R2 = 1718.87 / dor
    eg = tvd - kop - R2
    eo = dh + R1
    goe = degrees(atan(eg / eo))
    og = sqrt(eg**2 + eo**2)
    of = R1-R2
    gof = degrees(acos(og / og))
    theta = 180 - goe- gof
    tvd_eob = kop + R1 * sin(radians(theta))
    if unit == 'ingles':
        md_eob = kop + (theta / bur) * 100
    else:
        md_eob = kop + (theta / bur) * 30
    dh_eob = R1 - abs(R1 * cos(radians(theta)))
    tan_len = sqrt(og**2 - of**2)
    if unit == 'ingles':
        md_sod = kop + (theta / bur) * 100 + tan_len
    else:
         md_sod = kop + (theta / bur) * 30 + tan_len

    if unit == 'ingles':
        md_total = kop + (theta / bur) * 100 + tan_len + (theta / dor) * 100
    else:
        md_total = kop + (theta / bur) * 30 + tan_len + (theta / dor) * 30

    output_H = Output_H(R1=R1, R2=R2, Theta=theta, TVD_EOB1=tvd_eob, Md_EOB1=md_eob, Dh_EOB1=dh_eob, \
                    Tan_len=tan_len,Md_SOB2=md_sod , Md_total=md_total)

    names = ['R1', 'R2', 'theta', 'tvd_EOB1', 'Md_EOB1', 'Dh_EOB1', 'Lengh_tan', 'Md_SOD2', 'Md_Total']
    for param , value in zip(names, output_H):
        if param == 'theta':
            print(f"{param} -> {value} degrees")
        else:
            print(f"{param} -> {value} ft")

# Call dataframe
if upload_file:
    df = pd.read_csv(upload_file)

# Call web app sections
if options == "Data":
    data(df)

elif options == "3D Plots":
    plot(df)

elif options == "Basic Calculations":
    st.subheader("**Select unit**")
    units = st.selectbox("Units", ("ingles", "metric"))
    if st.checkbox("J-well type"):
        st.subheader("**Enter input values**")
        kop = st.number_input("Enter kop value: ")
        tvd = st.number_input("Enter tvd value: ")
        dh = st.number_input("Enter dh value: ")
        bur = st.number_input("Enter bur value")
        st.subheader("**Show results**")
        well_J(Data(tvd, kop, bur, dh), units)

    elif st.checkbox("S-well type"):
        st.subheader("**Enter input values**")
        kop = st.number_input("Enter kop value: ")
        tvd = st.number_input("Enter tvd value: ")
        dh = st.number_input("Enter dh value: ")
        bur = st.number_input("Enter bur value")
        dor = st.number_input("Enter dor value")
        st.subheader("**Show results**")
        well_S(Data_S(tvd, kop, bur, dor, dh), units)
    elif st.checkbox("H-well type"):
        st.subheader("**Enter input values**")
        kop = st.number_input("Enter kop value: ")
        tvd = st.number_input("Enter tvd value: ")
        dh = st.number_input("Enter dh value: ")
        bur = st.number_input("Enter bur value")
        dor = st.number_input("Enter dor value")
        st.subheader("**Show results**")
        well_H(Data_H(tvd, kop, bur, dor, dh), units)
