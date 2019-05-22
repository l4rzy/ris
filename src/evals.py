import numpy as np
import cv2
import os

def showImage(img):
    cv2.imshow('dst',img)
    while True:
        k = cv2.waitKey(0)
        if k == ord('q'): # wait for 'q' to exit
            cv2.destroyAllWindows()
            return

"""
Compares 2 images based on color histograms of 2 images
"""
class Histogram:
    name = 'histogram'

    @staticmethod
    def channels():
        return ('b', 'g', 'r')

    @staticmethod
    def index(db, datadir):
        print('HISTOGRAM indexing ...')
        try:
            for (root, dirs, files) in os.walk(datadir):
                for f in files:
                    if f.endswith('jpg') or f.endswith('png'):
                        path = os.path.join(root, f)
                        val = Histogram.calc(path)
                        db.insert(Histogram.name, path, val)
        except Exception as e:
            raise e
        print('done.')

    @staticmethod
    def calc(fname):
        print(f'HISTOGRAM calculating {fname}')
        try:
            img = cv2.imread(fname, cv2.IMREAD_COLOR)
        except Exception as e:
            raise e

        ret = np.zeros((3, 256))
        for i, col in enumerate(Histogram.channels()):
            hist = cv2.calcHist([img], [i], None, [256], [0, 256])
            ret[i] = np.copy(hist.reshape(1, -1)[0])

        ## ret is now a combination of 3 vectors for 3 color histogram b g r respectively
        return ret

    ## this calculates the euclidian distance between 2 vectors
    @staticmethod
    def distance(h1, h2):
        ret = 0
        for i in range(3):
            d = np.sqrt(np.sum((h1[i] - h2[i])**2))
            ret += d

        return ret


"""
Compares 2 images using SIFT
"""
class SIFT:
    name = 'sift'
    sift = cv2.xfeatures2d.SIFT_create()
    matcher = cv2.BFMatcher()

    ## default config
    ratio = 0.75
    match_k = 2

    @staticmethod
    def index(db, datadir):
        print('SIFT indexing ...')
        try:
            for (root, dirs, files) in os.walk(datadir):
                for f in files:
                    if f.endswith('jpg') or f.endswith('png'):
                        path = os.path.join(root, f)
                        kp, desc = SIFT.calc(path)
                        db.insert(SIFT.name, path, val)
        except Exception as e:
            raise e
        print('done.')

    @staticmethod
    def calc(fname):
        ## load image as a grayscale image
        print(f'SIFT calculating {fname}')
        try:
            img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
        except Exception as e:
            raise e

        kp, desc = SIFT.sift.detectAndCompute(img,None)
        #out = cv2.drawKeypoints(img, kp, img)

        #showImage(out)
        return (kp, desc)

    @staticmethod
    def distance(desc1, desc2):
        matches = SIFT.matcher.knnMatch(desc1, desc2, k=SIFT.match_k)
        print(len(matches), "matches")

        good = []

        for m,n in matches:
            print(type(m), n.distance)


class ResNet:
    pass
