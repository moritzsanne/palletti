import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image, ImageOps
from sklearn.cluster import KMeans
import colorsys
import requests
from io import BytesIO
#turn off interactive plotting
plt.ioff()
import math

def capDimensions(width, height, maxPixels):
    pixels = width * height
    if (pixels <= maxPixels):
        return (width, height)

    ratio = float(width) / height
    scale = math.sqrt(float(pixels) / maxPixels)
    height2 = int(float(height) / scale)
    width2 = int(ratio * height / scale)
    return (width2, height2)

class Pallette:
    def __init__(self,url=None,local_file=None,n_clusters=6,n_samples=5000):
        # Turn interactive plotting off
        plt.ioff()
        #load image
        if url is not None:
            response = requests.get(url)
            pil_img = Image.open(BytesIO(response.content))
        elif local_file is not None:
            pil_img = Image.open(local_file)
        else:
            raise ValueError("Neither Local file nor URL to image file set.")
        
        pil_img = ImageOps.flip(pil_img)
        self.img = np.array(pil_img)        
        self.n_clusters = n_clusters
        self.width = self.img.shape[1]
        self.height = self.img.shape[0]
        self.resized_image = np.array(pil_img.resize(capDimensions(self.width,self.height,n_samples)))

        self.cluster()
    def cluster(self,sort_by="V"):
        #cluster rgb values using K-means

        samples = self.resized_image.reshape((self.resized_image.shape[0] * self.resized_image.shape[1], 3))
        clusters = KMeans(n_clusters = self.n_clusters)
        clusters.fit(samples[0:-1:1,:])
        self.pallette_rgb = clusters.cluster_centers_.astype('int')
        
        #convert cluster centers to hsv for intuitive sorting
        self.pallette_hsv = [colorsys.rgb_to_hsv(c[0],c[1],c[2]) for c in self.pallette_rgb]
        
        #Sort dominat colors
        if sort_by == "H" or sort_by == "Hue":
            key = 0
        elif sort_by == "S" or sort_by == "Saturation":
            key = 1
        else:
            key = 2
        self.pallette_hsv.sort(key=lambda x:x[key])
        self.pallette_rgb = np.array([colorsys.hsv_to_rgb(c[0],c[1],c[2]) for c in self.pallette_hsv])
        
    def get_figure(self):
        #palette attributes
        pallette_height = 0.05*self.height
        rect_width = self.width/self.n_clusters
        spacing = 10
        
        dpi = matplotlib.rcParams['figure.dpi']
        figsize = self.width / float(dpi), self.height / float(dpi)
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
        plt.imshow(self.img,origin="lower")
        for i in range(0,self.n_clusters):
            rect1 = matplotlib.patches.Rectangle((i*rect_width,-pallette_height-spacing), rect_width, pallette_height, color=self.pallette_rgb[i][:]/255)
            ax.add_patch(rect1)
        plt.xlim([0, self.width])
        plt.ylim([-200, self.height])
        ax.axis('off')
        return fig,ax
        
    def plot(self):
        fig, ax = self.get_figure()
        plt.show()
        
    def save(self,filename):
        fig, ax = self.get_figure()
        fig.savefig(filename,dpi="figure")
        plt.close(fig)
