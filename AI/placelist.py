import requests
import re

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, ' ', text)

# NCP 콘솔에서 복사한 클라이언트ID와 클라이언트Secret 값
client_id = "aMULIGwFk5vpOTzbZkV3"
client_secret = "EWFQtlQdip"


# 주소 텍스트

university = {"한양대", "서울대", "연세대", "고려대", "서강대", "성균관대", "홍익대", "중앙대", "경희대", "한국외대", "시립대","건국대", "동국대",}
building = {"학부 및 대학원 건물",
    "도서관",
    "학생회관",
    "연구소 및 실험실",
    "체육시설",
    "기숙사",
    "행정 건물",
    "식당 및 카페테리아"}

query_list = []

for univ in university:
    for build in building:
        query_list.append(univ + build)

display = 5
start = 1

endpoint = "https://openapi.naver.com/v1/search/local.json"


# 헤더
headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret,
}



# 요청

for query in query_list:
    url = f"{endpoint}?query={query}&display={display}&start={start}"
    res = requests.get(url, headers=headers) 
    # JSON 데이터 파싱
    data = res.json()


    titles = [remove_html_tags(item['title']) for item in data['items'] if item['category'] == "대학교>부속건물" or "대학교>식당" or "대학교>건물"]

    for title in titles:
        campus_index = title.find("캠퍼스")
        if campus_index != -1:
            print(title[campus_index + len("캠퍼스"):])
        else:
            print(title)

    # for j in range(0,len(titles)):
    #     campus_index = title.find("캠퍼스")
    #     print(titles[j])