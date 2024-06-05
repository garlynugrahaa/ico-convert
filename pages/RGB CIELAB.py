import numpy as np
import streamlit as st
from PIL import Image

def rgb2xyz(image):
    imageR = image[:,:,0]
    imageG = image[:,:,1]
    imageB = image[:,:,2]
    
    m, n = imageR.shape

    k = [[0.49, 0.31, 0.20],
         [0.17697, 0.82140, 0.01063],
         [0.00, 0.01, 0.99]
        ]
    
    Ix = np.zeros((m, n))
    Iy = np.zeros((m, n))
    Iz = np.zeros((m, n))

    for i in range(m):
        for j in range(n):
            rgb = np.array([imageR[i,j], imageG[i,j], imageB[i,j]])
            xyz = (1 / 0.17697) * np.dot(k, np.array(rgb))
            Ix[i, j] = xyz[0]
            Iy[i, j] = xyz[1]
            Iz[i, j] = xyz[2]

    imageXYZ = np.zeros((m, n, 3))
    imageXYZ[:,:,0] = Ix
    imageXYZ[:,:,1] = Iy
    imageXYZ[:,:,2] = Iz

    f = imageXYZ

    return f

def xyz2rgb(image):
    imageX = image[:,:,0]
    imageY = image[:,:,1]
    imageZ = image[:,:,2]

    m, n = imageX.shape

    k = [[0.41847, -0.15866, -0.082835],
         [-0.091169, 0.25243, 0.015708],
         [0.00092090, 0.0025498, 0.17860]
        ]
    
    Ir = np.zeros((m, n))
    Ig = np.zeros((m, n))
    Ib = np.zeros((m, n))
    
    for i in range(m):
        for j in range(n):
            xyz = np.array([imageX[i,j], imageY[i,j], imageZ[i,j]])
            rgb = np.dot(k, np.array(xyz))
            Ir[i, j] = np.uint8(rgb[0])
            Ig[i, j] = np.uint8(rgb[1])
            Ib[i, j] = np.uint8(rgb[2])
    
    imageRGB = np.zeros((m, n, 3))
    imageRGB[:,:,0] = Ir
    imageRGB[:,:,1] = Ig
    imageRGB[:,:,2] = Ib

    f = imageRGB

    return f

def fLab(q):
    qn = float(q)

    if qn > 0.008856:
        x = pow(qn, 1/3)
    else:
        x = (7.787 * qn) + (16 / 116)
    return x

def rgb2cielab(image):
    ImageXYZ = rgb2xyz(image)
    ImageX = ImageXYZ[:,:,0]
    ImageY = ImageXYZ[:,:,1]
    ImageZ = ImageXYZ[:,:,2]

    m,n = ImageX.shape

    xn = 0.95047
    yn = 1
    zn = 1.08883

    IL = np.zeros((m, n))
    Ia = np.zeros((m, n))
    Ib = np.zeros((m, n))

    for i in range(m):
        for j in range(n):
            IL[i, j] = 116*fLab(ImageY[i, j] / yn)-16
            Ia[i, j] = 500*(fLab(ImageX[i, j] / xn) - fLab(ImageZ[i, j] / zn))
            Ib[i, j] = 200*(fLab(ImageY[i, j] / yn) - fLab(ImageZ[i, j] / zn))

    ImageLab = np.zeros((m, n, 3))
    ImageLab[:,:,0] = IL
    ImageLab[:,:,1] = Ia
    ImageLab[:,:,2] = Ib

    f = ImageLab

    return f

def cielab2rgb(image):
    imageL = image[:,:,0]
    imagea = image[:,:,1]
    imageb = image[:,:,2]

    m,n = imageL.shape

    iY = np.zeros((m, n))
    iX = np.zeros((m, n))
    iZ = np.zeros((m, n))

    xw = 0.9505
    yw = 1.0000
    zw = 1.0890

    for i in range(m):
        for j in range(n):
            L = imageL[i, j]
            a = imagea[i, j]
            b = imageb[i, j]

            fY = ((L + 16) / 116) ** 3

            if fY <= 0.008856:
                fY = (L / 903.3)

            fY = fLab(fY)
            iY[i, j] = fY * yw

            fX = (a / 500) + fY

            if fX > 0.008856:
                fX = fX ** 3
            else:
                fX = (fX - 16 / 116) / 7.787

            iX[i, j] = fX * xw

            fZ = fY - (b / 200)

            if fZ > 0.008856:
                fZ = fZ ** 3
            else:
                fZ = (fZ - 16 / 116) / 7.787

            iZ[i, j] = fZ * zw
            
    
    imageXYZ = np.zeros((m, n, 3))
    imageXYZ[:,:,0] = iX
    imageXYZ[:,:,1] = iY
    imageXYZ[:,:,2] = iZ
    imageRGB = xyz2rgb(imageXYZ)
    f = np.clip(imageRGB, 0, 1)

    return f

st.title("RGB and CIELAB Converter")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Original Image')
    st.write("Converting image...")
    image_array = np.array(image) / 255.0  # normalize pixel values
    image_lab = rgb2cielab(image_array)
    image_rgb = cielab2rgb(image_lab)
    st.write("Conversion complete!")
    st.image(image_lab, caption='RGB to LAB Image', clamp=True)
    st.image(image_rgb, caption='LAB to RGB Image', clamp=True)