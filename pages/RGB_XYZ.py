import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st

def RGB2XYZ(img):
    TransformMatrix = np.array([[0.412453, 0.357580, 0.180423], [0.212671, 0.715160, 0.072169], [0.019334, 0.119193, 0.950227]])
  
    arr = np.array(img)
    arr = arr / 255.0

    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    
    RGB = np.stack((r, g, b), axis = 2)
    XYZ = np.dot(RGB, TransformMatrix)
    
    return Image.fromarray((XYZ * 255).astype(np.uint8), mode='RGB')

def XYZ2RGB(img):
    arr = np.array(img)
    arr = arr / 255.0

    x, y, z = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    XYZ = np.stack((x, y, z), axis=2)

    RGB2XYZMatrix = np.array([[0.412453, 0.357580, 0.180423], [0.212671, 0.715160, 0.072169], [0.019334, 0.119193, 0.950227]])
    XYZ2RGBMatrix = np.linalg.inv(RGB2XYZMatrix)

    RGB = np.dot(XYZ, XYZ2RGBMatrix)

    return Image.fromarray((RGB * 255).astype(np.uint8), mode='RGB')

st.title("RGB and XYZ Converter")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Original Image')
    st.write("Converting image...")
    image_array = np.array(image) # normalize pixel values
    image_xyz = RGB2XYZ(image_array)
    image_rgb = XYZ2RGB(image_xyz)
    st.write("Conversion complete!")
    st.image(image_xyz, caption='RGB to XYZ Image', clamp=True)
    st.image(image_rgb, caption='XYZ to RGB Image', clamp=True)