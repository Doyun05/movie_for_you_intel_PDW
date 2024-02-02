import  pandas as pd #라이브러리는 데이터 처리 및 분석을 위한 기능을 제공
from sklearn.metrics.pairwise import linear_kernel #선형 커널을 사용하여 두 벡터 간의 유사도를 계산하는 기능
from scipy.io import mmread #희소 행렬 데이터를 읽어로는 기능을 제공
import pickle #객체 직렬화를 위한 기능을 제공
from konlpy.tag import Okt #한국어 형태소분석기를 사용
from gensim.models import Word2Vec #클래스는 단어 임베딩을 위한 Word2Vec 모델을 구현한 기능을 제공

#영화 추천 시스템에서 유사도 점수를 기반으로 영화를 추천하는 기능을 수행
def getRecommendation(cosine_sim):
    #매개 변수를 입력으로 받는다. 영화들 간의 코사인 유사도 행렬을 나타낸다.
    simScore = list(enumerate(cosine_sim[-1]))
    #행렬의 마지막(마지막 영화)의 유사도 점수를 인덱스와 함께 리스트로 저장
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    #리스트를 key 파라미터를 기준으로 내림차순으로 정렬
    simScore = simScore[:11]
    #자기 자신을 포함한 총 11편의 영화를 추출

    movieIdx = [i[0] for i in simScore]
    #상위 유사도 영화들의 인덱스를 저장
    recmovieList = df_reviews.iloc[movieIdx, 0]
    #데이터프레임에서 movieIdx에 해당하는 영화들의 제목을 추출하여 저장
    return recmovieList[1:11]
    #첫 번째 영화를 제외한 10개의 영화를 반환, 자기 자신을 제외한 상위 10개의 영화를 추천

df_reviews = pd.read_csv('./cleaned_one_review.csv')
#파일을 읽어와 df_reviews에 저장
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

#영화 index 이용추천
#ref_idx = 10
#print(df_reviews.iloc[ref_idx, 0])
#consine_sim = linear_kernel(Tfidf_matrix[ref_idx], Tfidf_matrix)
#print(consine_sim[0])
#print(len(consine_sim))
#recommendation = getRecommendation(consine_sim)
#print(recommendation)

# keyword 이용

embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')
keyword = '드래곤'
sim_word = embedding_model.wv.most_similar(keyword, topn=10)
words = [keyword]
for word, _ in sim_word:
    words.append(word)
setence = []
count = 10
for word in words:
    setence = setence + [word] * count
    count -= 1
setence = ' '.join(setence)
print(setence)
setence_vec = Tfidf.transform([setence])
cosine_sim = linear_kernel(setence_vec, Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)

print(recommendation)


























