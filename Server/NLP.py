from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import load_model
import h5py
import numpy as np
from konlpy.tag import Okt
import pickle

okt = Okt()
with open("C:\\Users\\dongjin\\Desktop\\src_tokenizer_modified.pickle", 'rb') as handle:
    src_tokenizer = pickle.load(handle)
    
bilstm_model = load_model("C:\\Users\\dongjin\\Desktop\\NLP_model_modified.h5")


def processing(string):
    random_sequence = okt.morphs(string)
    X_random = src_tokenizer.texts_to_sequences([random_sequence])
    X_random = pad_sequences(X_random, padding='post', maxlen=32)

    # 예측 수행
    y_random_predicted = bilstm_model.predict(np.array(X_random))
    y_random_predicted = np.argmax(y_random_predicted, axis=-1)

    answer_pos = ""
    answer_neg = ""
    
    np.array([y_random_predicted])
    y_random_predicted = y_random_predicted[0]
    for word, idx in zip(random_sequence, y_random_predicted):
        if idx == 3 or idx == 5:
            answer_neg += word
        elif idx == 4 or idx == 2:
            answer_pos += word
    return answer_pos, answer_neg
