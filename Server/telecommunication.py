import socket
import NLP
import path
import difflib

HOST = '0.0.0.0'  # 모든 인터페이스에서 연결
PORT = 1234     # 사용할 포트 번호

word_list = ["학술정보관", "복지관", "제사공학관", "제삼공학관", "제이공학관", "제일학술관", "컨퍼러스홀", "정문", "셔틀콕", "제이과기관", "본관", "경상관", "국제문화관", "기숙사", "제일과기관","1과기관", "4공학관","3공학관","1공학관","1학술관","2과기관"]

def most_similar_word(input_word, word_list):
    # 입력 단어와 리스트의 단어들 간의 유사도 계산.
    similarity_scores = [difflib.SequenceMatcher(None, input_word, word).ratio() for word in word_list]

    # 높은 유사도의 단어 추출 및 유사성 계산.
    max_similarity = max(similarity_scores)
    most_similar_index = similarity_scores.index(max_similarity)
    most_similar_word = word_list[most_similar_index]

    return most_similar_word, max_similarity

def handle_client(conn, addr):
    print('클라이언트와 연결됨:', addr)
    try:
        #while True:
        original = conn.recv(1024)
        if not original:
            print('클라이언트가 연결을 종료.')
            return


        data = original.decode("utf-8")
        print('수신된 데이터:', data)
        split_data = data.split("|")

        string = split_data[0]
        latitude = float(split_data[1])
        longitude = float(split_data[2])
            

        dest_pos, dest_neg = NLP.processing(string)
        print(f"processed_positive_word : {dest_pos}, processed_negative_word : {dest_neg}")

        if dest_pos == "" and dest_neg == "":
            conn.sendall("None".encode())

        elif dest_neg == "":
            most_similar_des_pos, max_similarity_pos = most_similar_word(dest_pos, word_list)

            if(max_similarity_pos < 0.5):
                conn.sendall("None".encode())
            
            else:
                print(f"most similar positive word : {most_similar_des_pos}, max_similarity_pos : {max_similarity_pos}") 
                print(f"most similar negative word : False, max_similarity_neg : False")
                way_to_des = path.returnpath(most_similar_des_pos, latitude, longitude, None)
                print("path:", way_to_des)
                    
                conn.sendall(way_to_des.encode())

        else:
            most_similar_des_pos, max_similarity_pos = most_similar_word(dest_pos, word_list)
            most_similar_des_neg, max_similarity_neg = most_similar_word(dest_neg, word_list)
            if(max_similarity_pos < 0.5):
                conn.sendall("None".encode())
            
            else:

                print(f"most similar positive word : {most_similar_des_pos}, max_similarity_pos : {max_similarity_pos}") 
                print(f"most similar negative word : {most_similar_des_neg}, max_similarity_neg : {max_similarity_neg}")

                way_to_des = path.returnpath(most_similar_des_pos, latitude, longitude, most_similar_des_neg)
                print("path:", way_to_des)

                conn.sendall(way_to_des.encode())
    except Exception as e:
        print(f"에러 발생: {e}")
    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("서버 시작, 클라이언트 연결 대기 중...")
        
        while True:
            conn, addr = s.accept()
            print("클라이언트 연결 수락")
            handle_client(conn, addr)

if __name__ == "__main__":
    start_server()

'''
import socket
import NLP
import path
import difflib


HOST = '0.0.0.0'  # 모든 인터페이스에서 연결을 수락
PORT = 1234     # 사용할 포트 번호

NLP.processing("나는 복지관 가고 싶어")

word_list = ["학술정보관", "복지관", "제사공학관", "제삼공학관", "제일공학관", "제일학술관", "컨퍼러스홀", "정문", "셔틀콕", "제이과기관", "본관", "경상관", "국제문화관", "기숙사", "제일과기관","1과기관", "4공학관","3공학관","1공학관","1학술관","2과기관"]

def most_similar_word(input_word, word_list):
    # 입력 단어와 리스트의 단어들 간의 유사도를 계산합니다.
    similarity_scores = [difflib.SequenceMatcher(None, input_word, word).ratio() for word in word_list]

    # 가장 높은 유사도를 가지는 단어를 찾습니다.
    max_similarity = max(similarity_scores)
    most_similar_index = similarity_scores.index(max_similarity)
    most_similar_word = word_list[most_similar_index]

    return most_similar_word, max_similarity



while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("서버 시작, 클라이언트 연결 대기 중...")
        
        conn, addr = s.accept()
        with conn:
            print('클라이언트와 연결됨:', addr)
            while True:
                original = conn.recv(1024)
                if not original:
                    print('클라이언트가 연결을 종료했습니다.')
                    break
                data = original.decode("utf-8")
                print('수신된 데이터:', data)
                split_data = data.split("|")
                string = split_data[0]
                latitude = float(split_data[1])
                longitude = float(split_data[2])
                
                    
                dest_pos = NLP.processing(string)
                print(f"processed_word : {dest_pos}")
                
                #dest_pos, dest_neg= NLP.processing(string) # revise to extract the destination
                most_similar_des_pos, max_similarity_pos = most_similar_word(dest_pos, word_list)
                #most_similar_des_neg, max_similarity_neg = most_similar_word(dest_neg, word_list)

                print(f"most similar positive word : {most_similar_des_pos}, most similar negative word : {False}") 
               
                way_to_des = path.returnpath(most_similar_des_pos, latitude, longitude)
                print("path:", way_to_des)

                conn.sendall(way_to_des.encode()) # 수정된 위치에 sendall 메서드 호출
'''