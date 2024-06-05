import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st
import colorsys

def RGB2HSV(img):
    arr = np.array(img)
    arr = arr / 255.0

    h = np.zeros_like(arr[:, :, 0])
    s = np.zeros_like(arr[:, :, 0])
    v = np.zeros_like(arr[:, :, 0])

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            r = arr[i, j, 0]
            g = arr[i, j, 1]
            b = arr[i, j, 2]
            h[i, j], s[i, j], v[i, j] = colorsys.rgb_to_hsv(r, g, b)

    h = (h * 255).astype(np.uint8)
    s = (s * 255).astype(np.uint8)
    v = (v * 255).astype(np.uint8)

    HSV = np.stack((h, s, v), axis=2)

    return Image.fromarray(HSV)

def HSV2RGB(image):
    arr = np.array(image)
    arr = arr / 255.0

    h = arr[:, :, 0] * 360.0
    s = arr[:, :, 1]
    v = arr[:, :, 2]

    c = v * s
    x = c * (1 - abs((h / 60.0) % 2 - 1))
    m = v - c
    
    r, g, b = 0, 0, 0

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if 0 <= h[i, j] < 60:
                r, g, b = c[i, j], x[i, j], 0
            elif 60 <= h[i, j] < 120:
                r, g, b = x[i, j], c[i, j], 0
            elif 120 <= h[i, j] < 180:
                r, g, b = 0, c[i, j], x[i, j]
            elif 180 <= h[i, j] < 240:
                r, g, b = 0, x[i, j], c[i, j]
            elif 240 <= h[i, j] < 300:
                r, g, b = x[i, j], 0, c[i, j]
            elif 300 <= h[i, j] < 360:
                r, g, b = c[i, j], 0, x[i, j]

            arr[i, j, 0] = (r + m[i, j]) * 255.0
            arr[i, j, 1] = (g + m[i, j]) * 255.0
            arr[i, j, 2] = (b + m[i, j]) * 255.0

            
    img_result = Image.fromarray(arr.astype(np.uint8))
    img_result.save("hasilke2.png")

    return img_result

st.title("RGB and CMY Converter")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Original Image')
    st.write("Converting image...")
    image_array = np.array(image) / 255.0
    image_hsv = RGB2HSV(image_array)
    image_rgb = HSV2RGB(image_hsv)
    st.write("Conversion complete!")
    st.image(image_hsv, caption='RGB to HSV Image', clamp=True)
    st.image(image_rgb, caption='HSV to RGB Image', clamp=True)