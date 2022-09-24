from cmath import inf
import os
import numpy as np
from PIL import Image
from skimage.color import rgb2hsv, hsv2rgb
from skimage.io import imread
from skimage.transform import rescale, resize, downscale_local_mean
from sklearn.cluster import KMeans
import time
from localdb import LocalDB


db = LocalDB()
start = time.time()
print('Loading image...')
path = "/home/pi/covers/"

dir_list = os.listdir(path)

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb
print('clustering...')
if len(dir_list) == 1:
    img_path = path + dir_list[0]
    img = imread(img_path)

    # id is the unique track id, I'm just chopping the path off here
    id = img_path[22:-4]


    # album covers come in at 512, 512, 3 channels, this takes too long, so we'll downsample
    # 64x64 is faster, but for >6 clusters we'll downsample to 32x32

    image_16 = rescale(img, 0.03125, multichannel=True)

    wcss_last = 0
    delta_last = np.inf
    pc_last = 0
    done = False

    # reshape the images to a list of colors

    x16 = np.array(image_16).reshape(-1,3)

    def get_cluster_centers(i, image, wcss):
        global wcss_last, delta_last, pc_last, done
        rnd = time.time()
        kmeans = KMeans(n_clusters=int(i), random_state=0).fit(image)
        wcss_iter = kmeans.inertia_

        delta = round(wcss_iter - wcss_last)
        perc_change = round((float(wcss_iter)/wcss)*100, 2)

        p = kmeans.cluster_centers_
        hsv = rgb2hsv(p)
        for j in range(len(hsv)):
            hsv[j][1] = min(hsv[j][1]*2, 1)
            hsv[j][2] = hsv[j][2]*0.75

        rgb = hsv2rgb(sorted(hsv, key=lambda x: x[1], reverse=True))

        hexColors = [('#'+rgb_to_hex((int(rgb[j][0]*255), int(rgb[j][1]*255), int(rgb[j][2]*255)))) for j in range(len(rgb))]
        db.update_cover(id, hexColors)
        if delta < inf:
            print(str(i)+ ' cluster(s) '+str(round(delta,2))+str(round(time.time() - rnd))+' = '+str(perc_change)+'% - '+str(pc_last-perc_change)+'')
        if perc_change < 5:
            print('quitting - ', perc_change)
            return False

        wcss_last = wcss_iter
        pc_last = perc_change

        dir_list = os.listdir(path)
        npath = path + dir_list[0]
        if img_path != npath:
            print('new image')
            return False
        return True
    # run some baselines to get a comparison
    get_cluster_centers(1, x16, 1)
    db.set_current(id)

    image_64 = rescale(img, 0.125, multichannel=True)
    x64 = np.array(image_64).reshape(-1,3)
    get_cluster_centers(1, x64, 1)
    wcss_first64 = wcss_last


    for i in range(2,9):
        ret = get_cluster_centers(i, x64, wcss_first64)
        if ret == False:
            done = True
            break



    print('total:'+str(round(time.time() - start)))
