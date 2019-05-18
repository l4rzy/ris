import numpy as np
import cv2

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
    @staticmethod
    def channels():
        return ('b', 'g', 'r')

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
    ## default config
    @staticmethod
    def config():
        blocksize = 2
        ksize     = 3
        k         = 0.05

        return (blocksize, ksize, k)

    @staticmethod
    def calc(fname):
        ## load image as a grayscale image
        print(f'SIFT calculating {fname}')
        try:
            img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
        except Exception as e:
            raise e

        config = SIFT.config()

        ## find corners by harris
        sift = cv2.xfeatures2d.SIFT_create()
        kp = sift.detect(img,None)
        out = cv2.drawKeypoints(img, kp, img)

        showImage(out)

    @staticmethod
    def distance(f1, f2):
        pass

class ResNet:
    pass
