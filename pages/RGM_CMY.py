import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st

def rgb2cmy(img):
    arr = np.array(img)
    arr = arr / 255.0

    c = arr[:, :, 0]
    m = arr[:, :, 1]
    y = arr[:, :, 2]

    r = (1 - c) * 255.0
    g = (1 - m) * 255.0
    b = (1 - y) * 255.0

    RGB = np.stack((r, g, b), axis = 2)

    return Image.fromarray(RGB.astype(np.uint8))

def cmy2rgb(img):
    arr = np.array(img)
    arr = arr / 255.0

    c = arr[:, :, 0]
    m = arr[:, :, 1]
    y = arr[:, :, 2]

    r = (1 - c) * 255.0
    g = (1 - m) * 255.0
    b = (1 - y) * 255.0

    RGB = np.stack((r, g, b), axis = 2)

    return Image.fromarray(RGB.astype(np.uint8))

st.title("RGB and CMY Converter")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Original Image')
    st.write("Converting image...")
    image_array = np.array(image) / 255.0
    image_cmy = rgb2cmy(image_array)
    image_rgb = cmy2rgb(image_cmy)
    st.write("Conversion complete!")
    st.image(image_cmy, caption='RGB to CMY Image', clamp=True)
    st.image(image_rgb, caption='CMY to RGB Image', clamp=True)