// 칼만 필터의 간단한 구현 예시
#include <stdio.h>

// 칼만 필터 구조체 정의
typedef struct {
    float q; // 프로세스 노이즈 공분산
    float r; // 측정 노이즈 공분산
    float x; // 추정된 값
    float p; // 추정 공분산
    float k; // 칼만 이득
} kalman_state;

/* 이 구조체는 칼만 필터의 상태를 저장합니다.
q는 프로세스 노이즈 공분산으로, 시스템 모델의 불확실성을 나타냅니다.
r은 측정 노이즈 공분산으로, 측정값의 불확실성을 나타냅니다.
x는 현재 상태의 추정값입니다.
p는 추정 공분산으로, 추정값의 불확실성을 나타냅니다.
k는 칼만 이득으로, 예측과 측정 사이의 가중치를 결정합니다. */

// 칼만 필터 초기화
void kalman_init(kalman_state *state, float init_x, float init_p, float q, float r) {
    state->q = q;
    state->r = r;
    state->x = init_x;
    state->p = init_p;
}

/* 이 함수는 칼만 필터를 초기화합니다.
초기 상태 추정값(init_x)과 추정 공분산(init_p)을 설정합니다.
프로세스 노이즈(q)와 측정 노이즈(r)도 초기화합니다. */

// 칼만 필터 업데이트
void kalman_update(kalman_state *state, float measurement) {
    // 예측 업데이트
    state->p = state->p + state->q;

    // 칼만 이득 계산
    state->k = state->p / (state->p + state->r);

    // 새로운 측정값으로 상태 업데이트
    state->x = state->x + state->k * (measurement - state->x);

    // 오차 공분산 업데이트
    state->p = (1 - state->k) * state->p;
}

/* 예측 단계에서는 추정 공분산을 업데이트합니다. 여기서는 단순히 프로세스 노이즈를 더합니다.
칼만 이득을 계산합니다. 이는 예측 공분산과 측정 노이즈의 비율로 결정됩니다.
새로운 측정값을 사용하여 상태 추정값을 업데이트합니다. 여기서는 칼만 이득을 사용하여 새로운 측정값과 현재 추정값 사이의 차이를 조정합니다.
마지막으로 오차 공분산을 업데이트합니다. 이는 새로운 추정값의 불확실성을 나타냅니다. */