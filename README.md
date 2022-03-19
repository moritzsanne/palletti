# palletti
Palletti is a small python package, that allows to analyse the dominant colors of an images using K-Means clustering.

Example:

```
import palletti

img = "example/clark-van-der-beken-tqss4wZILRQ-unsplash.jpg"
image_pallete = palletti.Pallette(local_file=img,n_clusters=6,n_samples=100000)
image_pallete.plot()

```




The object also return the pallete as an array, in either rgb or hsv colorspace:
```
image_pallete.pallette_rgb

#array([[ 25.,  51.,  46.],
#       [116., 122., 104.],
#       [208., 180., 138.],
#       [207., 210., 203.],
#       [140., 209., 248.],
#       [ 90., 191., 249.]])

image_pallete.pallette_hsv

#[(0.4679487179487179, 0.5098039215686274, 51),
# (0.22222222222222224, 0.14754098360655737, 122),
# (0.09999999999999999, 0.33653846153846156, 208),
# (0.23809523809523805, 0.03333333333333333, 210),
# (0.5601851851851851, 0.43548387096774194, 248),
# (0.5607966457023061, 0.6385542168674698, 249)]

```

You can also save an image including the plotted pallette:

```
image_pallete.save("img_incl_pallette.jpg")
```