from __future__ import print_function
warned_of_error = False
import csv
import nltk
from nltk.corpus import stopwords
import pygame
import simplejson
from pytagcloud import create_tag_image, make_tags


def create_cloud (oname, words,maxsize=120, fontname='Lobster'):

    tags = make_tags(words, maxsize=maxsize)
    create_tag_image(tags, oname, size=(1800, 1200), fontname=fontname)