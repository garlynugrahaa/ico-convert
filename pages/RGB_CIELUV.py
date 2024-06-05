import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def RGB2LUV(img):
    arr = np.array(img)
    arr = arr / 255.0

    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    RGB = np.stack((r, g, b), axis=2)

    RGB2LUVMatrix = np.array([[0.299, 0.587, 0.114], [-0.14713, 0.28886, 0.436], [0.615, -0.51499, -0.10001]])

    LUV = np.dot(RGB, RGB2LUVMatrix)
    LUV[:, :, 0] = LUV[:, :, 0] * 100
    LUV[:, :, 1:] = LUV[:, :, 1:] * 354.0 - np.array([134.0, -140.0])[None, None, :]

    return Image.fromarray((LUV * 255).astype(np.uint8), mode='RGB')

def LUV2RGB(img):
    arr = np.array(img)
    arr = arr / 255.0
    arr[:, :, 1:] = (arr[:, :, 1:] + np.array([134.0, -140.0])[None, None, :]) / 354.0

    l, u, v = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    LUV = np.stack((l, u, v), axis=2)

    LUV2RGBMatrix = np.array([[3.24096994, -1.53738318, -0.49861076], [-0.96924364, 1.8759675, 0.04155506], [0.05563008, -0.20397696, 1.05697151]])

    RGB = np.dot(LUV, LUV2RGBMatrix)
    RGB = np.clip(RGB, 0, 1) * 255

    return Image.fromarray(RGB.astype(np.uint8), mode='RGB')

st.title("RGB and CIELUV Converter")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Original Image')
    st.write("Converting image...")
    image_array = np.array(image) # normalize pixel values
    image_luv = RGB2LUV(image_array)
    image_rgb = LUV2RGB(image_luv)
    st.write("Conversion complete!")
    st.image(image_luv, caption='RGB to LUV Image', clamp=True)
    st.image(image_rgb, caption='LUV to RGB Image', clamp=True)