import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./reviews_kinolights.csv')
df.info()

df_stopwords = pd.read_csv('./stopwords.csv')
stopwords = list(df_stopwords['stopword'])

okt = Okt()

for review in df.reviews[:5]:
    review = re.sub('[^가-힣]',' ', review)
    tokened_review = okt.pos(review, stem=True)
    print(tokened_review)
















