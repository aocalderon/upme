from flask import Flask, send_file
import math
from PIL import Image
import numpy as np
import os.path
from io import BytesIO
from numba import jit

app = Flask(__name__)

SIZE = 256
RADIUS = 15.0
MAX_ITER = 2028
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'cache')

@jit
def wikipedia(n):
    if n%16 == 0:
        return [66, 30, 15]
    if n%16 == 1:
        return [25, 7, 26]
    if n%16 == 2:
        return [9, 1, 47]
    if n%16 == 3:
        return [4, 4, 73]
    if n%16 == 4:
        return [0, 7, 100]
    if n%16 == 5:
        return [12, 44, 138]
    if n%16 == 6:
        return [24, 82, 177]
    if n%16 == 7:
        return [57, 125, 209]
    if n%16 == 8:
        return [134, 181, 229]
    if n%16 == 9:
        return [211, 236, 248]
    if n%16 == 10:
        return [241, 233, 191]
    if n%16 == 11:
        return [248, 201, 95]
    if n%16 == 12:
        return [255, 170, 0]
    if n%16 == 13:
        return [204, 128, 0]
    if n%16 == 14:
        return [153, 87, 0]
    if n%16 == 15:
        return [106, 52, 3]

@jit
def color_map(n, t_re, t_im):
    module = np.sqrt(t_re + t_im)
    logAbs = np.log(module)
    continuous = 1 + n - np.log(logAbs) / np.log(2.0)
    index = int(np.floor(continuous))
    a = wikipedia(index)
    b = wikipedia(index + 1)
    p = 1 - (continuous - index)
    r = int(np.floor(p * a[0] + (1 - p) * b[0]))
    g = int(np.floor(p * a[1] + (1 - p) * b[1]))
    b = int(np.floor(p * a[2] + (1 - p) * b[2]))
    return [r,g,b]

@jit
def escape_time(re_0, im_0, maxiter):
    z_re = re_0;
    z_im = im_0;
    t_re = 0;
    t_im = 0;
    for n in range(maxiter):
        t_re = z_re * z_re
        t_im = z_im * z_im
        if t_re + t_im > RADIUS:
            return color_map(n, t_re, t_im)
        z_im = 2 * z_re * z_im + im_0
        z_re = t_re - t_im + re_0
    return [0,0,0]

@jit
def draw(xmin, xmax, ymin, ymax, width=SIZE, height=SIZE, maxiter=MAX_ITER):
    re_range = np.linspace(xmin, xmax, width)
    im_range = np.linspace(ymin, ymax, height)
    mandelbrot_array = np.zeros((width, height, 3), dtype=np.uint8)
    for i in range(width):
        for j in range(height):
            mandelbrot_array[i,j] = escape_time(re_range[i],im_range[j],MAX_ITER)
    return mandelbrot_array

def project(x, y, z):
    n = 2.0 ** z
    re = -.5 +  y / n * 2 - 1
    im =  -(x / n * 2) + 1
    return re, im

def create_image(z, x, y, filepath):
    re_min, im_min = project(x, y, z)
    re_max, im_max = project(x + 1, y + 1, z)
    mandelbrot_array = draw(re_min,re_max,im_min,im_max)
    image = Image.fromarray(mandelbrot_array, 'RGB')
    image.save(filepath)
    return image

@app.route('/mandelbrot')
@app.route('/mandelbrot/<int:z>/<int:x>/<int:y>', methods=['GET'])
def mandelbrot_view(z=0, x=0, y=0):
    filepath = os.path.join(CACHE_DIR, '%s-%s-%s.png' % (z,x,y))
    if os.path.isfile(filepath):
        image = Image.open(filepath)
    else:
        image = create_image(z, x, y, filepath)
    byte_io = BytesIO()
    image.save(byte_io, 'PNG')
    byte_io.seek(0)
    return send_file(byte_io, mimetype='image/png')

if __name__ == "__main__":
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    app.run()