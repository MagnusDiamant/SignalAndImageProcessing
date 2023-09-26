# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QkDNBYOqkCSxO0GNZlN-b3uD2XZ5_Yru
"""

# Assignment 1.1
from skimage.io import imread, imsave
import matplotlib.pyplot as plt

def gamma_transform(image, c, gamma, gray_flag):
    if gray_flag == True:
        return c*image**gamma
    else:
        return c*(image/255)**gamma

image = imread("/content/football.jpg", as_gray=True)
plt.imshow(image, cmap="gray")
plt.title("Gamma = 1")
plt.show()
plt.imshow(gamma_transform(image, 1, 0.5, True), cmap="gray")
plt.title("Gamma = 0.5")
plt.show()
plt.imshow(gamma_transform(image, 1, 2, True), cmap="gray")
plt.title("Gamma = 2")
plt.show()

# Assignment 1.2
import numpy as np

image = imread("autumn.tif")

def gamma_transformation_rgb(image, gamma):
    R = gamma_transform(image[:,:,0], 1, gamma, False)
    G = gamma_transform(image[:,:,1], 1, gamma, False)
    B = gamma_transform(image[:,:,2], 1, gamma, False)
    return np.dstack((R, G, B))

figure, ax = plt.subplots(1, 3, figsize=(10,10))
ax[0].imshow(image)
ax[1].imshow(gamma_transformation_rgb(image, 0.1))
ax[2].imshow(gamma_transformation_rgb(image, 3))
ax[0].set_title("Gamma = 1")
ax[1].set_title("Gamma = 0.1")
ax[2].set_title("Gamma = 3")
plt.show()

# Assignment 1.3
from skimage.color import rgb2hsv, hsv2rgb

def gamma_transform_hsv(image, gamma):
    image[:,:,2] = gamma_transform(image[:,:,2], 1, gamma, True)
    return image

image = imread("autumn.tif")
image_hsv = rgb2hsv(image)
image_rgb = hsv2rgb(gamma_transform_hsv(image_hsv, 0.1))
image_rgb2 = hsv2rgb(gamma_transform_hsv(image_hsv, 3.0))
fig, ax = plt.subplots(1, 3, figsize=(10,10))
ax[0].imshow(image)
ax[1].imshow(image_rgb)
ax[2].imshow(image_rgb2)
ax[0].set_title("Gamma = 1")
ax[1].set_title("Gamma = 0.1")
ax[2].set_title("Gamma = 3")
plt.show()

from typing import SupportsComplex
#2.1
import math
import matplotlib as mpl

def histo(im):
  pic1 = np.sort(im.reshape(-1))
  his = {}
  counter = 0
  b = np.arange(0,256)
  for i in b:
    his[i] = 0
    for j in range(counter, len(pic1)):
      if(pic1[j] <= i):
        his[i] += 1
        counter = j + 1
      else:
        break
  fig = plt.figure()
  plt.bar(list(his.keys()), list(his.values()), width=1, color="k")
  plt.title("Histogram with 256 bins")
  ax = fig.add_axes([0.160, -0.05, 0.705, 0.1])
  cb = mpl.colorbar.ColorbarBase(ax, orientation='horizontal', cmap=plt.cm.gray)
  cb.set_ticks([])
  counter = 0
  div = sum([his[x] for x in his])
  cum = {}
  for i in b:
    his[i] += counter
    counter = his[i]
    cum[i] = counter/div
  fig = plt.figure()
  plt.bar(list(cum.keys()), list(cum.values()), width=1, color="k")
  plt.title("Cumulative histogram")
  ax = fig.add_axes([0.160, -0.05, 0.705, 0.1])
  cb = mpl.colorbar.ColorbarBase(ax, orientation='horizontal', cmap=plt.cm.gray)
  cb.set_ticks([])
  return cum

pic1 = imread("pout.tif")
b = histo(pic1)

def float_image(image, cum):
  flattened_image = image.reshape(-1)
  for idx, p in enumerate(flattened_image):
    flattened_image[idx] = cum[p]*255
  return flattened_image.reshape(image.shape)        
pic1 = imread("pout.tif")
fig, ax = plt.subplots(1, 2, figsize=(10,10))
ax[0].imshow(pic1, cmap="gray")
ax[0].set_title("Before transformation")
pic2 = float_image(pic1, histo(pic1))
bins = histo(pic2)
ax[1].imshow(pic2, cmap="gray")
ax[1].set_title("After transformation")
plt.show()

# Assignment 2.3
def float_image(l, cum):
    prev = 0
    for c in cum:
        if(l > cum[c]):
            prev = c
        elif(l == cum[c]):
            return c
        else:
            return prev

image = imread("pout.tif")
cum = histo(image)


float_image(0.5, cum)

# Assignment 2.4
def histo_matching(x, y):
    bins_x = histo(x)
    bins_y = histo(y)
    flatten = x.reshape(-1)

    for i, f in enumerate(flatten):
        flatten[i] = float_image(bins_x[f], bins_y)
  
    return flatten.reshape(x.shape)

from skimage import exposure
# Assignment 2.5
noise = np.arange(0,256)
image = imread("pout.tif")
fig, ax = plt.subplots(1, 3, figsize=(10,10))
ax[0].imshow(image, cmap="gray")
ax[0].set_title("Original image")
ax[1].imshow(histo_matching(image, noise), cmap="gray")
ax[1].set_title("Image after Histogram matching")
ax[2].imshow(exposure.equalize_hist(image), cmap="gray")
ax[2].set_title("Image after Histogram Equalizer")
plt.show()



# Assignment 3.1
from scipy import ndimage
from scipy import signal
from skimage import util
import timeit

image = imread("eight.tif", as_gray=True)
image_sp = util.random_noise(image, mode="s&p", amount=0.1)
image_gaus = util.random_noise(image, mode="gaussian", var=0.01)

median_sp = signal.medfilt2d(image_sp, kernel_size=11)
mean_sp = ndimage.filters.convolve(image_sp, np.full((10,10), 1.0/100))
median_gaus = signal.medfilt2d(image_gaus, kernel_size=11)
mean_gaus = ndimage.filters.convolve(image_gaus, np.full((10,10), 1.0/100))

fig, ax = plt.subplots(2, 3, figsize=(12,8))
ax[0, 0].imshow(image_sp, cmap="gray")
ax[0, 0].set_title("Salt & Pepper noise")
ax[0, 1].imshow(median_sp, cmap="gray")
ax[0, 1].set_title("Salt & Pepper noise (Median filter)")
ax[0, 2].imshow(mean_sp, cmap="gray")
ax[0, 2].set_title("Salt & Pepper noise (Mean filter)")
ax[1, 0].imshow(image_gaus, cmap="gray")
ax[1, 0].set_title("Gaussian noise")
ax[1, 1].imshow(median_gaus, cmap="gray")
ax[1, 1].set_title("Gaussian noise (Median filter)")
ax[1, 2].imshow(mean_gaus, cmap="gray")
ax[1, 2].set_title("Gaussian noise (Mean filter)")
plt.show()

mean_sp_25 = ndimage.filters.convolve(image_sp, np.full((100,100), 1.0/10000))
median_sp_25 = signal.medfilt2d(image_sp, kernel_size=25)
median_gaus_25 = signal.medfilt2d(image_gaus, kernel_size=25)
mean_gaus_25 = ndimage.filters.convolve(image_gaus, np.full((100,100), 1.0/10000))
fig, ax = plt.subplots(2, 4, figsize=(12,6))
ax[0, 0].imshow(mean_sp, cmap="gray")
ax[0, 0].set_title("Salt & Pepper noise \n(Mean filter N = 10)")
ax[1, 0].imshow(mean_sp_25, cmap="gray")
ax[1, 0].set_title("Salt & Pepper noise \n(Mean filter N = 25)")
ax[1, 1].imshow(median_sp_25, cmap="gray")
ax[1, 1].set_title("Salt & Pepper noise \n(Median filter N = 25)")
ax[0, 1].imshow(median_sp, cmap="gray")
ax[0, 1].set_title("Salt & Pepper noise \n(Median filter N = 10)")
ax[0, 2].imshow(mean_gaus, cmap="gray")
ax[0, 2].set_title("Gaussian noise \n(Mean filter N = 10)")
ax[1, 2].imshow(mean_gaus_25, cmap="gray")
ax[1, 2].set_title("Gaussian noise \n(Mean filter N = 25)")
ax[0, 3].imshow(median_gaus, cmap="gray")
ax[0, 3].set_title("Gaussian noise \n(Median filter N = 10)")
ax[1, 3].imshow(median_gaus_25, cmap="gray")
ax[1, 3].set_title("Gaussian noise \n(Median filter N = 25)")
plt.show()

y = []
z = []
for i in range(1, 25):
    y.append(timeit.timeit("ndimage.filters.convolve(image_sp, np.full(({},{}), {}))".format(i, i, 1.0/i*i), setup="import numpy as np; from scipy import ndimage; from skimage import util; from skimage.io import imread; image = imread('eight.tif', as_gray=True); image_sp = util.random_noise(image, mode='s&p', amount=0.1)", number=100))
    if i % 2 != 0:
        z.append(timeit.timeit("signal.medfilt2d(image_sp, kernel_size={})".format(i), setup="from scipy import signal; import numpy as np; from scipy import ndimage; from skimage import util; from skimage.io import imread; image = imread('eight.tif', as_gray=True); image_sp = util.random_noise(image, mode='s&p', amount=0.1)", number=100))

plt.plot(np.arange(1,25), y)
plt.xlabel("Kernel_size")
plt.ylabel("Time in seconds")
plt.title("Experiment for mean filter")
plt.show()
x = [1,3,5,7,9,11,13,15,17,19,21,23]
plt.plot(x, z)
plt.xlabel("Kernel_size")
plt.ylabel("Time in seconds")
plt.title("Experiment for median filter")
plt.show()

import cv2 as cv
def filter_gauss(image, k, s):
  blur = cv.GaussianBlur(image, (k,k), s)
  return blur
image = cv.cvtColor(cv.imread("eight.tif"), cv.COLOR_BGR2GRAY)
noiseImage = util.random_noise(image, mode="s&p", amount=0.05)
g5 = filter_gauss(noiseImage, 3, 5)
g10 = filter_gauss(noiseImage, 9, 5)
g25 = filter_gauss(noiseImage, 27, 5)
fig, ax = plt.subplots(2, 2, figsize=(8,6))
ax[0, 0].imshow(noiseImage, cmap="gray")
ax[0, 0].set_title("Noise")
ax[0, 1].imshow(g5, cmap="gray")
ax[0, 1].set_title("Gaussian filter N = 3, sigma = 5")
ax[1, 0].imshow(g10, cmap="gray")
ax[1, 0].set_title("Gaussian filter N = 9, sigma = 5")
ax[1, 1].imshow(g25, cmap="gray")
ax[1, 1].set_title("Gaussian filter N = 27, sigma = 5")
plt.show()

#3.3
image = cv.cvtColor(cv.imread("eight.tif"), cv.COLOR_BGR2GRAY)
noiseImage = util.random_noise(image, mode="s&p", amount=0.05)
g5 = filter_gauss(noiseImage, 9, 3)
g10 = filter_gauss(noiseImage, 27, 9)
g25 = filter_gauss(noiseImage, 81, 27)
fig, ax = plt.subplots(2, 2, figsize=(8,6))
ax[0, 0].imshow(noiseImage, cmap="gray")
ax[0, 0].set_title("Noise")
ax[0, 1].imshow(g5, cmap="gray")
ax[0, 1].set_title("Gaussian filter N = 9, sigma = 3")
ax[1, 0].imshow(g10, cmap="gray")
ax[1, 0].set_title("Gaussian filter N = 27, sigma = 9")
ax[1, 1].imshow(g25, cmap="gray")
ax[1, 1].set_title("Gaussian filter N = 81, sigma = 27")
plt.show()

# Assignment 4.2
def gaussian(r2, sigma):
    return np.exp(-0.5*r2/sigma**2)

def bilateral_filter(image, w_size, sigma, tau):
    half_width = int(w_size/2)
    res  = image*0.1
    weights = np.ones(image.shape)
    for shift_x in range(-half_width,half_width):
        for shift_y in range(-half_width,half_width):
            w1 = gaussian(shift_x**2+shift_y**2, sigma)
            offset = np.roll(image, [shift_y, shift_x], axis=[0,1] )
            temp_w = w1*gaussian((offset-image)**2, tau)
            res += offset*temp_w
            weights += temp_w
    return res/weights


# Assignment 4.3
image = imread("eight.tif", as_gray=True)
image = util.random_noise(image, mode="gaussian", var=0.01).astype(np.float32)
image1 = bilateral_filter(image, 50.0, 1000.0, 1000.0)
image2 = bilateral_filter(image, 50.0, 0.1, 15.0)
image3 = bilateral_filter(image, 50.0, 10.0, 0.1)
image4 = bilateral_filter(image, 50.0, 100, 0.0001)
image5 = bilateral_filter(image, 50.0, 0.0001, 100)

fig, ax = plt.subplots(2, 3, figsize=(12,8))
ax[0, 0].imshow(image, cmap="gray")
ax[0, 1].imshow(image1, cmap="gray")
ax[0, 2].imshow(image2, cmap="gray")
ax[1, 0].imshow(image3, cmap="gray")
ax[1, 1].imshow(image4, cmap="gray")
ax[1, 2].imshow(image5, cmap="gray")
ax[0, 0].set_title("Original image")
ax[0, 1].set_title("sigma = 1000, tau = 1000")
ax[0, 2].set_title("sigma = 0.1, tau = 15")
ax[1, 0].set_title("sigma = 10, tau = 0.1")
ax[1, 1].set_title("sigma = 100, tau = 0.0001")
ax[1, 2].set_title("sigma = 0.0001, tau = 100")
plt.show()