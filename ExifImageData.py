#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Encapsulation of Exif data readed from image file

@author Juanma Sánchez
"""
import os
import logging
from PIL import Image, ExifTags
from exif import Image as eImage


logging.basicConfig(level=logging.DEBUG)

class ExifImageData:
    _imgName = None
    _imgFullName = None
    _exifDict = {}
    _exifTags = []

    def __init__(self, imgName):
        self.load_exif(imgName)

    def load_exif(self, fileName):
        '''Function that load Exif data from image given
                its file name'''
        if os.path.isabs(fileName):
            logging.info("[isabs=true] fileName = " + fileName)
            self._imgName = os.path.basename(fileName)
            logging.debug("_imgName: " + self._imgName)
            self._imgFullName = fileName

        else:
            sImgPath = os.path.curdir
            logging.info("sImgPath = " + sImgPath)
            self._imgFullName = os.path.join(sImgPath, fileName)
            logging.info("[isabs=false] _imgFullName: " + self._imgFullName)

        with open(self._imgFullName, 'rb') as img_file:
            eimg = eImage(img_file)

        logging.info("has_exif(): " + str(eimg.has_exif))
        logging.warning("___________________________")

        #self.load_exif_values()
        self._exifTags = sorted(eimg.list_all())
        #print(self._exifTags)
        self._exifDict = {
            (self._exifTags[i], eimg.get(self._exifTags[i])) for i in range(0, len(self._exifTags))
        }
        logging.debug("EXIF data:" + str(self._exifDict))

if __name__ == '__main__':
    eid = ExifImageData("/home/juxmix/PycharmProjects/ImageUtils/Imágenes/20220608_181933.jpg")


