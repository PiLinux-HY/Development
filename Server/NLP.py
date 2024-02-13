from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import load_model
import h5py
import numpy as np
from konlpy.tag import Okt

okt = Okt()
src_tokenizer = Tokenizer(filters=None, lower=False)

def processing(string):
    bilstm_model = load_model("ai_model.h5")

    random_sequence = okt.morphs(string)
    X_random = src_tokenizer.texts_to_sequences([random_sequence])
    X_random = pad_sequences(X_random, padding='post', maxlen=20)

    # 예측 수행
    y_random_predicted = bilstm_model.predict(np.array(X_random))
    y_random_predicted = np.argmax(y_random_predicted, axis=-1)

    np.array([y_random_predicted])
    y_random_predicted = y_random_predicted[0]

    for idx, word in zip(y_random_predicted, random_sequence):
        if index_list[idx] != 1 :
            answer += word

    return answer
