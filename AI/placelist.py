import requests
import re

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, ' ', text)

def get_campus_name(address):
    # 주소에서 학교 이름을 추출합니다.
    campus_name = ""
    address_parts = address.split()
    for i, part in enumerate(address_parts):
        if part.endswith("대") or part.endswith("대학교"):
            campus_name = " ".join(address_parts[i:])
            break
    return campus_name.strip()

# NCP 콘솔에서 복사한 클라이언트ID와 클라이언트Secret 값
client_id = "aMULIGwFk5vpOTzbZkV3"
client_secret = "EWFQtlQdip"

# 대학교 리스트
universities = ["한양대에리카", "한양대",  "서울대", "연세대", "고려대", "서강대", "성균관대", "홍익대", "중앙대", 
                "경희대", "한국외대", "시립대", "건국대", "동국대"] 

# 대학교 주변 모든 건물 리스트
buildings =["부속건물", "셔틀콕", "공학관","과학기술관","경상관", "사범", "디자인관", "체육관", "도서관", "약학대", "학생회관", "기숙사", "대학원", "체육시설", "복지관", "창의인재원","행복관",
             "연구소", "예체능", "실험실", "행정 건물", "식당", "카페", "인문관", "예술관", "디자인센터", "음악관", "철학관", "사회과학관",
             "의과대","창업센터","인문학관", "생명과학관", "국제관", "교육관", "산학협력관", "정보통신관", "산업기술관", "창업보육관", "정류장"] 

query_list = []

for univ in universities:
    for build in buildings:
        query_list.append(f"{univ} {build}")

display = 5
start = 1
total_results = 0

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
    data = res.json()

    # 캠퍼스 이름과 건물 이름을 가져오는 부분 수정
    for item in data['items']:
        if item['category'].startswith("대학교>"):
            address = item['address']
            campus_name = get_campus_name(address)
            building_name = remove_html_tags(item['title'])
            print(campus_name + " " + building_name)  # 수정된 부분

# 페이징 처리
while start + display < total_results:
    start += display
    for query in query_list:
        url = f"{endpoint}?query={query}&display={display}&start={start}"
        res = requests.get(url, headers=headers) 
        data = res.json()

        # 캠퍼스 이름과 건물 이름을 가져오는 부분 수정
        for item in data['items']:
            if item['category'].startswith("대학교>"):
                address = item['address']
                campus_name = get_campus_name(address)
                building_name = remove_html_tags(item['title'])
                print(campus_name + " " + building_name)  # 수정된 부분