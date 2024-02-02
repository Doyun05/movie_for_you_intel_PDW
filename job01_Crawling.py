from selenium import webdriver #웹 브라우저를 자동으로 조작하는 도구
from selenium.webdriver.common.by import By #다양한 요소를 찾는 방법을 지정 XPath CSS 웹 요소를 찾을 수 있다.
from selenium.webdriver.common.keys import Keys #특수 키를 보내거나 키 조합을 사용하기 위함
from selenium.webdriver.chrome.service import Service as ChromeService #버전에 맞는 서비스를 사용하기 위한 클래스
from selenium.webdriver.chrome.options import Options as ChromeOptions #브라우저의 옵션을 설정하기 위한 클래스
from webdriver_manager.chrome import ChromeDriverManager #Driver의 버전을 자동으로 관리할 수 있다.
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException #이를 사용하여 요소를 찾을 수 없거나, 요소가 더 이상 유효하지 않을 때 예외 처리를 할 수 있다.
import pandas as pd #데이터를 다루기 위한 패키지 데이터프레임 형태로 데이터를 처리하고 분석하는데 사용
import re #정규 표현식을 사용하기 위한 모듈인 re를 import 시간 지연 타이밍등...
import time #시간과 관련된 기능을 사용하기 위한 모듈인 time
import datetime #날짜와 시간을 다루기 위한 모듈 날짜 및 시간 정보를 생성 조작 및 포맷팅

options = ChromeOptions() #클래스의 인스턴스인 크롬 브라우저의 옵션을 설정할 수 있다.
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
#사용자 에이전트는 브라우저가 서번에게 자신의 정보를 전달하기 위한 식별자
options.add_argument('user-agent=' + user_agent) #메서드를 사용하여 사용자 에이전트 옵션을 추가
options.add_argument("lang=ko_KR") #메서드를 사용하여 언어 옵션을 추가 크롬 언어를 한국어로 설정
# options.add_argument('headless')
# options.add_argument('window-size=1920X1080')

service = ChromeService(executable_path=ChromeDriverManager().install())
#클래스의 인스턴스인 service를 생성 자동으로 다운로드하고 실행 가능한 경로  반환
driver = webdriver.Chrome(service=service, options=options)
#생성자 driver라는 WebDriver 인스턴스를 생성 options 인수로 클롬 브라우저의 옵션을 설정하고  이를 통해 실험

start_url = 'https://m.kinolights.com/discover/explore'
#start_url 변수에 접속하려는 웹 페이지의 URL이 저장
button_movie_tv_xpath = '//*[@id="contents"]/section/div[3]/div/div/div[3]/button'
#버튼의 xpath가 저장, 웹 페이지에서 요소를 찾는 경로를 나타내는 문자열
button_movie_xpath = '//*[@id="contents"]/section/div[4]/div[2]/div[1]/div[3]/div[2]/div[2]/div/button[1]'
button_ok_xpath = '//*[@id="applyFilterButton"]'
#각각의 버튼에 대한 XPath를 저장하고 있다.
driver.get(start_url) #호출하여 접속하려는 웹 페이지로 이동
time.sleep(0.5) #너무 빠르면 에러가 나기 때문에 잠시 지연
button_movie_tv = driver.find_element(By.XPATH, button_movie_tv_xpath)
#해당하는 버튼 요소를 찾아, By.XPATH는 XPath를 사용하여 요소를 찾는 방법, 찾은 버튼 요소를 button 변수에 할당
driver.execute_script('arguments[0].click();', button_movie_tv)
#JavaScrip를 실행 movie_tv 요소를 클릭 이렇게 함으로써 해당 버튼을 클릭하는 작업
time.sleep(0.5)
button_movie = driver.find_element(By.XPATH, button_movie_xpath)
#해당하는 버튼 요소를 찾아 Xpath를 사용 요소를 찾는 방법을 지정하는 역할, 찾은
driver.execute_script('arguments[0].click();', button_movie)
#JavaScript를 실행하여 button_movie 요소를 클릭 이렇게 함으로써 해당 버튼을 클릭하는 작업
time.sleep(1)#웹 페이지 변화를 기다리기 위한 대기 시간 1초동안 지연
button_ok = driver.find_element(By.XPATH, button_ok_xpath)
#ok에 해당하는 버튼 요소를 찾고 XPATH를 사용하여 요소를 찾는 방법을 지정하는 역할
driver.execute_script('arguments[0].click();', button_ok)
#JavaScript를 실행하여 button_ok 요소를 클릭 해당 버튼을 클릭하는 작업을 수행

#--웹 페이지에서 스크롤을 내리고 스크롤이 끝까지 도달할 때까지 일정 시간 동안 대기하는 작업--
for i in range(25):
    #25번 반복하는 루프(스크롤을 25번 내리는 작업)
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    #JavaScript를 실행하여 현재 웹페이지의 끝까지 스크롤을 내리는 역할 0은 가로 스크롤 위치,
     #scrollHeight 문서의 전체 높이를 나타낸다. 세로 스크롤을 문서의 전체 높이까지 내림
    time.sleep(1)
list_review_url = []
movie_titles = []
#빈 리스트로 초기화 이후 코드에서 이 리스트에 데이터를 추가할 수 있다.

#--웹 페이지에서 영화 리뷰의 URL과 영화 제목을 추출하는 작업을 수행하는 코드
for i in range(1, 1000):
    base = driver.find_element(By.XPATH, f'//*[@id="contents"]/div/div/div[3]/div[2]/div[{i}]/a').get_attribute("href")
    #XPath를 사용하여 웹 페이지에서 i에 해당하는 요소의 href 속성 값을 추출 base변수에 저장
    #해당 요소의 링크 URL을 나타낸다. URL은 list_review 리스트에 추가된다.
    list_review_url.append(f"{base}/reviews")#속성 값을 읽어온다.
    #완전한 리뷰 URL을 생성하고 이를 list_review 리스트에 추가
    title = driver.find_element(By.XPATH, f'//*[@id="contents"]/div/div/div[3]/div[2]/div[{i}]/div/div[1]').text
    #XPath를 사용하여 웹 페이지에서 i에 해당하는 요소의 텍스트 값을 추출하여 title 변수에 저장
    movie_titles.append(title)
    #추출한 영화 제목을 movie 리스트에 추가


print(list_review_url[:5]) #리스트의 처음 5개 요소를 출력, URL중 처음 5개를 확인
print(len(list_review_url)) #리스트의 길이 영화 리뷰 URL의 총 개수를 확인
print(movie_titles[:5]) #영화 제목중 처음 5개를 확인
print(len(movie_titles)) #리스트의 길이를 출력, 추출한 영화 제목의 총 개수를 확인

reviews = [] #추출한 리뷰를 저장하는 용도로 사용
for idx, url in enumerate(list_review_url[500:551]):
    #리스트의 500번 인덱스부터 550번 인덱스까지의 요소를 순회하는 반복문
    driver.get(url) #웹 드라이버를 사용하여 영화 리뷰 페이지를 불러오는 역할
    time.sleep(1) #1초의 지연을 추가 페이지가 로드되는 동안 잠시 대기
    review = '' #빈 문자열인 review를 생성 추출한 리뷰를 임시로 저장
    for i in range(1, 31):
        #리뷰를 추출할 웹 페이지의 구조가 반복되는 패턴을 가지고 있다.
        review_title_xpath = '//*[@id="contents"]/div[2]/div[2]/div[{}]/div/div[3]/a[1]/div'.format(i)
        #i 값을 이용하여 리뷰 제목의 XPath를 동적으로 생성
        review_more_xpath = '//*[@id="contents"]/div[2]/div[2]/div[{}]/div/div[3]/div/button'.format(i)
        #i 값을 이용하여 "더보기" 버튼의 XPath를 생성하는 역할
        try:
            review_more = driver.find_element(By.XPATH, review_more_xpath)
            #웹 드라이버를 사용하여 "더보기" 버튼 요소를 찾는다.
            driver.execute_script('arguments[0].click();', review_more)
            #메서드를 사용하여 JavaScript를 실행하여 "더보기" 버튼을 클릭
            time.sleep(1)
            review_xpath = '//*[@id="contents"]/div[2]/div[1]/div/section[2]/div/div'
            #해당 페이지에서 리뷰 내용을 가리키는 XPath를 생성하는 역할
            review = review + ' ' + driver.find_element(By.XPATH, review_xpath).text
            #웹 드라이버를 사용하여 리뷰 내용을 추출하여 review변수에 추가, 리뷰의 내용이 하나의 문자열로 저장
            driver.back() #이전 페이지로 돌아간다.
            time.sleep(1)

        except NoSuchElementException as e:
            #예외가 발생한 경우에 대한 예외 처리를 시작
            print('더보기', e) #"더보기" 버튼을 찾지 못한 경우에 대한 오류 메세지를 출력
            try:
                review = review + ' ' + driver.find_element(By.XPATH, review_title_xpath).text
            except:
                print('review title error')

        except StaleElementReferenceException as e:
            print('stale', e)


        except :
            print('error')

    print(review)
    reviews.append(review)
#print(reviews[:5])
print(len(reviews))

df = pd.DataFrame({'title':movie_titles[500:551], 'reviews':reviews})
today = datetime.datetime.now().strftime('%Y%m%d')
df.to_csv('./Crawling_Data/reviews_550_.csv'.format(today), index=False)

















