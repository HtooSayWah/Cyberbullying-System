from segmentation import *
from normalization import *
from model import *

def classification(text):
    nor_text = main(text)    
    segment_text = TokenizeWithLSMA(nor_text)
    bully_words = Classify(segment_text)
    return bully_words;
