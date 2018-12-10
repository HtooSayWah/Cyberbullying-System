from segmentation import *
from normalization import *
from model import *

def init(text):
    nor_text = main(text)    
    segment_text = TokenizeWithLSMA(nor_text)
    bully_words = Classify(segment_text)
    print(bully_words)
    
    

