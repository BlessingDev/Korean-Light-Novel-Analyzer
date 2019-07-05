# Korean-Light-Novel-Analyzer

![](https://img.shields.io/badge/license-GPL-blue.svg)

## Requirements
* 본 프로그램은 ![Pycharm IDE](https://www.jetbrains.com/pycharm/)에서 프로그래밍 되었습니다. Pycharm에서 올바르게 작동합니다.
* requirements.txt를 참고합니다.
* mecab-python 모듈은 ![이 곳](https://cleancode-ws.tistory.com/97)을 참고하여 설치합니다.

## 사용법
### 실행
main.py를 실행하는 것으로 프로젝트를 실행할 수 있습니다.

```
    cui_main(v, g, bc, bs, otbs, storer)
    #gui_main(v, g, bc, bs, otbs, storer)
```
main.py의 제일 마지막 두 라인에서 cui를 사용할지 gui를 사용할지 결정할 수 있습니다.<br>
gui는 pyqt5를 필요로 합니다.

### 라노베 데이터 내려받기
라노베 데이터는 용량이 매우 큰 관계로 깃허브에 업로드돼 있지 않습니다. 아래의 방법에 따라 라노베 정보를 내려받을 수 있습니다.

#### cui
```
------라이트 노벨 분석기 v. 0.2------
1. renew
2. ordinary_set
3. search
4. 훈련용 셋 만들기
5. 검색 정확도 시각화
6. 장르-단어 그래프
7. 장르 분류기 학습
8. 책 검색
9. 책간 거리 계산하기
10. 가까운 책 보기
11. XOR 네트워크 실험
12. 프로그램 종료
13. 이하 자유
--------------------------------------
무엇을 선택하시겠습니까? 1
```
**1. renew** 메뉴를 선택하는 것으로 가능합니다.

#### gui
![](https://lh3.googleusercontent.com/oK9uFMmWKQG6Vw4_gsSnEWWG7BgX3yEhqvZ1FBffm-bcvg4NsXLz7xuYVigepC3YwGQ2TGRf_XdS4R8PqvJFBnHXJ0RRBm1BWp2JSlZYYJ7FKnXCkkjMo83fd3s4fhUw6yZyl4rrQRr-ZJNHDlOSZe6m9YfvvhjhNxm22MtugLnH97QB-lXWn4W7p3a4nTz_6vz8oyfmI1v6HAKMWuB3khMd_Hy0nVUI2WWeqzQuRVeVHmgZvxNNWVu56jDM4waeWFEx-7zOn0Mja6GRRQva1mJvmHK4ZOSlutH59_p5SGIaly4iMEkBLXFGFhDi2JjiJGnXfnpLQdGdMJRFvvo0A1BAF9ROPQSIWU3pFTABJ3dFhYKjQxlThAprkGRieCIYq5wcRMJXcfVMMioZYymUa1eF_D_pDXKJTAfvQLdbAi2zBnYq6PM2wZub1rdeT2-tkvWT7YGRR8T18y5WhuUIFK61bBQOKHRK0iQMLU-lb8nzXUok1hKUTperR6yMyg4rgoGCiudAAnvyDReLZW4sf6FkezzeCrQfNvMfAC4w152My-Z9QkXtjFIkVxE-QD2W-uSe50StZwMwTFAf_fhxGSi5WHsKi7iFKmu83mayyVhpnT1aRgHH3-PuyRsqiToqzNWlm_EIOQzPL8TbfT2gL7d6_k3BgyE=w567-h568-no)

특정기간 책 크롤 메뉴를 선택,

![](https://lh3.googleusercontent.com/kdtx7vr4YxeqtpDBd5Ot7VYWSReW-z_Ip1Dhyqg0sRV36B8NLlLOTyKDJx99atPuZt92QuZeLFXMYeEDtlf0i6GGFoSOb3OqPdWw6C4HgG58OBeqRLLBLdZiCj6oJHoMWXp-RLaC13NqEw4Vnb-IaNkAdaDJ7a-SqwgsLCVtzeTzN8e9fUSpGDr36i8u6GIhw83GnPj5V3Ej0WoolJFmetQag-ET-Zw-7MOMKoAOgRMNN5hhW5D29Ub9DhMBq_WeTZXsDabMzdJoq2ADncLBrhxBnWU2nktMuzXO8Ld1et27hlqMM7S73wusIiJ-arv_W0Qb0PDxRhmMEXV0MOXMwfj8qtq9exFOuW2Z_EA811PZgrDroYJlCGZ0_BXsvYWSJ5mldhRYByCryWcZFAGU95k_mJiFzWzLePnr4NQ5xk5pOG0u7ng3ofvwECioEDKmYGI_6mRkl_xBz7YYEZu4Ut-x0f4tuCDi95ZP00Y34sIlmUH-Zg-0KcfS7K2U5lwyjMu-Gj10v5G2nGytNM7xu94x6eUs0gdEOIRqLmNILW0ZaQq8loFDK01yVrxkWnDS5h688QvyPuu569ZuyLHjcYEp6etwkNIKKy9Jb9-A3mZTt7jeY5xInBUYTvNtGCsuLg9BtAM_yrHHvjB1LVh6tGKc2cn65ik=w572-h612-no)

아무것도 체크하지 않고 **확인** 버튼을 누르는 것으로 가능합니다.

### 라노베 정보 파일 저장하기
내려받은 라노베 정보는 아래와 같은 절차로 pc에 저장됩니다.
#### cui
```
------라이트 노벨 분석기 v. 0.2------
1. renew
2. ordinary_set
3. search
4. 훈련용 셋 만들기
5. 검색 정확도 시각화
6. 장르-단어 그래프
7. 장르 분류기 학습
8. 책 검색
9. 책간 거리 계산하기
10. 가까운 책 보기
11. XOR 네트워크 실험
12. 프로그램 종료
13. 이하 자유
--------------------------------------
무엇을 선택하시겠습니까? 12
```
**12. 프로그램 종료** 메뉴를 선택하는 것으로 가능합니다.

#### gui
![](https://lh3.googleusercontent.com/kdtx7vr4YxeqtpDBd5Ot7VYWSReW-z_Ip1Dhyqg0sRV36B8NLlLOTyKDJx99atPuZt92QuZeLFXMYeEDtlf0i6GGFoSOb3OqPdWw6C4HgG58OBeqRLLBLdZiCj6oJHoMWXp-RLaC13NqEw4Vnb-IaNkAdaDJ7a-SqwgsLCVtzeTzN8e9fUSpGDr36i8u6GIhw83GnPj5V3Ej0WoolJFmetQag-ET-Zw-7MOMKoAOgRMNN5hhW5D29Ub9DhMBq_WeTZXsDabMzdJoq2ADncLBrhxBnWU2nktMuzXO8Ld1et27hlqMM7S73wusIiJ-arv_W0Qb0PDxRhmMEXV0MOXMwfj8qtq9exFOuW2Z_EA811PZgrDroYJlCGZ0_BXsvYWSJ5mldhRYByCryWcZFAGU95k_mJiFzWzLePnr4NQ5xk5pOG0u7ng3ofvwECioEDKmYGI_6mRkl_xBz7YYEZu4Ut-x0f4tuCDi95ZP00Y34sIlmUH-Zg-0KcfS7K2U5lwyjMu-Gj10v5G2nGytNM7xu94x6eUs0gdEOIRqLmNILW0ZaQq8loFDK01yVrxkWnDS5h688QvyPuu569ZuyLHjcYEp6etwkNIKKy9Jb9-A3mZTt7jeY5xInBUYTvNtGCsuLg9BtAM_yrHHvjB1LVh6tGKc2cn65ik=w572-h612-no)

**저장하기** 버튼을 누르는 것으로 가능합니다.

## 앞으로의 개발 사항
The purpose of this project is 
1. analyze Korean light novel publishing market.
2. auto-generate genre to light novels.
3. clustering based on genre, description, title, author, etc.

**The FINAL PURPOSE: light novel recommendation**
