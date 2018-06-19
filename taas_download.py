import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

#웹드라이버 셋팅
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', 'E:\\acc_alcohol')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk',"text/html")
driver = webdriver.Firefox(executable_path= 'C:/Program Files/Mozilla Firefox/geckodriver.exe',firefox_profile=profile)

#taas 홈페이지
URL = 'https://taas.koroad.or.kr/web/umt/lmt/initLogin.do'

#브라우저를 지정한 URL로 이동시킴
driver.get(URL)

#로그인창에 아이디/비번 입력 후 로그인 버튼 클릭
userid = driver.find_element_by_id('loginid')
userid.send_keys('skchang8')

#비번
userpwd = driver.find_element_by_id('loginpwd')
userpwd.send_keys('1fk1ah2sk38!')

#로그인 버튼
loginbtn = driver.find_element_by_id('loginbtn')
loginbtn.submit()

time.sleep(2)
#팝업 창 닫고 다시 돌아오기
mainpage = driver.window_handles[0]
popup = driver.window_handles[1]
driver.switch_to.window(popup)
driver.close()

driver.switch_to.window(mainpage)

#gis URL
URL = 'http://taas.koroad.or.kr/gis/mcm/mcl/initMap.do?menuId=GIS_GMP'
driver.get(URL)

#지역별 검색
partsearch = driver.find_element_by_id('menuPartSearch')
partsearch.click()

#음주운전사고 체크
acc_cls = driver.find_element_by_id('ptsRaf-ACC_CLS')
acc_cls.click()

acc_check = driver.find_element_by_xpath('//input[@value="ACC_CLS_06YN"]')
if not acc_check.is_selected():
    acc_check.click()

#사고내용 전 항목 체크

acdnt_gae = driver.find_element_by_id('ptsRaf-ACDNT_GAE_CODE')
acdnt_gae.click()

for i in range(1,5):
 acdnt_check = driver.find_element_by_xpath('//input[@value="0'+str(i)+'"]')
 if not acdnt_check.is_selected():
     acdnt_check.click()

close = driver.find_element_by_class_name('search-result-tit2')
close.click()

#시군구 for를 위한 리스트화
val = driver.find_element_by_id('ptsRafSigungu').text
sigungu = val.split('\n')

#시군구 선택
for i in sigungu:
    select_sigungu = Select(driver.find_element_by_xpath('//select[@id="ptsRafSigungu"]'))
    select_sigungu.select_by_visible_text(i)

    #검색
    search = driver.find_element_by_xpath('//p[@onclick="gis.srh.tas.raf.findRegionAccident(1)"]')
    search.click()

    time.sleep(10)

    #메인 재지정
    mainpage = driver.window_handles[0]

    #목록보기
    minibox = driver.find_element_by_class_name('btn-minibox')
    minibox.click()

    time.sleep(1)

    #최근 팝업창 이동
    popup = driver.window_handles[1]
    driver.switch_to.window(driver.window_handles[1])

    #다운로드
    download = driver.find_element_by_class_name('pop-btn04')
    download.click()

    time.sleep(7)
    driver.close()

    #메인 URL로
    driver.switch_to.window(mainpage)

    #html파일 csv로 저장
    fpath = 'E:\\acc_alcohol\\accidentInfoList'
    re_fpath = 'E:\\acc_alcohol\\'+ i
    rename = os.rename(fpath, re_fpath)
    to_csv = re_fpath + '.csv'

    html = open(re_fpath, encoding='UTF8').read()
    soup = BeautifulSoup(html, 'html.parser')

    thead = soup.select_one('thead')
    headers = [th.text for th in thead.select('tr th')]

    tbody = soup.select_one('tbody')
    with open(to_csv, 'w', newline='') as f:
        wr = csv.writer(f)
        wr.writerow(headers)
        for tr in tbody.find_all('tr'):
            wr.writerow([td.text for td in tr.find_all('td')])

driver.close()