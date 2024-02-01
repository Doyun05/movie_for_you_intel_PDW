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
time.sleep(0.5) #
button_movie_tv = driver.find_element(By.XPATH, button_movie_tv_xpath)
driver.execute_script('arguments[0].click();', button_movie_tv)
time.sleep(0.5)
button_movie = driver.find_element(By.XPATH, button_movie_xpath)
driver.execute_script('arguments[0].click();', button_movie)
time.sleep(1)
button_ok = driver.find_element(By.XPATH, button_ok_xpath)
driver.execute_script('arguments[0].click();', button_ok)
for i in range(25):
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(1)
list_review_url = []
movie_titles = []
for i in range(1, 1000):
    base = driver.find_element(By.XPATH, f'//*[@id="contents"]/div/div/div[3]/div[2]/div[{i}]/a').get_attribute("href")
    list_review_url.append(f"{base}/reviews")                                                          #속성 값을 읽어온다.
    title = driver.find_element(By.XPATH, f'//*[@id="contents"]/div/div/div[3]/div[2]/div[{i}]/div/div[1]').text
    movie_titles.append(title)

print(list_review_url[:5])
print(len(list_review_url))
print(movie_titles[:5])
print(len(movie_titles))

reviews = []
for idx, url in enumerate(list_review_url[500:551]):
    driver.get(url)
    time.sleep(1)
    review = ''
    for i in range(1, 31):
        review_title_xpath = '//*[@id="contents"]/div[2]/div[2]/div[{}]/div/div[3]/a[1]/div'.format(i)
        review_more_xpath = '//*[@id="contents"]/div[2]/div[2]/div[{}]/div/div[3]/div/button'.format(i)
        try:
            review_more = driver.find_element(By.XPATH, review_more_xpath)
            driver.execute_script('arguments[0].click();', review_more)
            time.sleep(1)
            review_xpath = '//*[@id="contents"]/div[2]/div[1]/div/section[2]/div/div'
            review = review + ' ' + driver.find_element(By.XPATH, review_xpath).text
            driver.back()
            time.sleep(1)

        except NoSuchElementException as e:
            print('더보기', e)
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

















