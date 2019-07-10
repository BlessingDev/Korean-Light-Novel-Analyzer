# Korean-Light-Novel-Analyzer

![](https://img.shields.io/badge/license-GPL-blue.svg)

## Requirements
* 본 프로그램은 [Pycharm IDE](https://www.jetbrains.com/pycharm/)에서 프로그래밍 되었습니다. Pycharm에서 올바르게 작동합니다.
* requirements.txt를 참고합니다.
* mecab-python 모듈은 [이 곳](https://cleancode-ws.tistory.com/97)을 참고하여 설치합니다.

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
![](https://lh3.googleusercontent.com/JeV3c8Rl9Tkc5PfWyB2v67QYEGhZr6BFRq1oZIoUlxk8FTAlpsvjqBym7QPU9jxcaZ-7mOrUb32pT2hp9rTYIFUdc804qPG3oMwakcPDdbV6vxbDTxY6fe8tcEIbKGavZ4a8DLxJEO9nAj9NF_PreQVBrPraYoUzCePr0h6dp_4HIfB3-mjcup5V_x5lRxku-wgHl4Gi-gM3gcD4SMKAFjN1_62AFz65-FrKVHgDXgl6QtaoBNIEQfBmHLe7LEcfNL_ctAttrD2tUjfy7QvA8heOqXR8EgBgxdKoUWyN2rJQg-5-RoKOcbyI4Mg8temyNH_l9YSMAlhGC1qpQMiN8JYz1Dv_hoAVYz7FQV0gGvF0VLy4D_AlZojTv78fsEXxnoOMiWpgLlbe3A3zz5iWySxrw4aPIwHyzbXVYHBN3Q7rG9Homat-mq8D2AmM6Fzx_nVNNiRlUv1t_aFJTmvCTt5Hmf_cDg87wtX7srZk4Y1CvH-Yc_kLScS6hFKjYpQ6-mRvos_S2Wbl1--xp8YupfEbnmBH1GSoymAk4Bx9daGJQPPxbRnJodxP36rtHSLctoIYM2E89eUlpQZC2iNawuiyUs2WXzXCWf3DhUlgMaLIN8-uAI0GxrFeDCEpt4Q5aBwdiK_7BPplgGYQ_f_hpcY6AhMKscI=w567-h568-no)

특정기간 책 크롤 메뉴를 선택하고, 오른쪽의 **확인** 버튼을 누릅니다.

![](https://lh3.googleusercontent.com/ZW2MXjCpfh31H6BDMZekrMxG2J25BydBYzqVH2MTA3yE1xL-mxuJahfgvXBLVe5ewH2wAJamNGEvQ2pudwu67dy0hFux8dO6-MMg13ZCCs_axsN3_yfYhxIriK2NyM2KpQMNFk1819LqNjK5gTWifoNONsCMFTuYcz8mW94sON_cgeJssQqaECeZlDbYcAfjinx-9Mg-9oYE-WjhqZ1410YONgd5AaIyOnnVeFYC6rl5-nr0EgCKKUOzqNLRjb8sFoNnNmldKxFxRLd313N4-hk852_vbdJEQPTMhattwkepMtmI9HP630rEWh1eiThe7HVnDHJ8HYCAdiFP3dj3_UUALThHhuUWnuEqeBRy7W6UXFrfIDJZHwLAeIEWw4cvVK0yvHKbv4hfC7WfrI0d8zw2bXuAHsqEwx-PBsKWVCby7fFbDB1t3WkW9lCk7ogeUmeJk7oNrmbQ1BNza0U3Rf5ItbWD3iDIaDlPnJGHhgPXJG77C116U4FMkiYHqHYzEz4mTF6nVI0-fyRZ_0omQ8zA4rVtX3aAjE1WgffIaQ7g2BbufaFvwgxNO6N3dY9s6IxKeUm22KPwaUI9t9XFBu2LtOWE8tqU_p8aiW47bOGdD5L2B3ji4BzmvkNkyIJkr2FiXh0YYrySLr6ZLCFBirt61wKeNKE=w572-h612-no)

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
![](https://lh3.googleusercontent.com/ZW2MXjCpfh31H6BDMZekrMxG2J25BydBYzqVH2MTA3yE1xL-mxuJahfgvXBLVe5ewH2wAJamNGEvQ2pudwu67dy0hFux8dO6-MMg13ZCCs_axsN3_yfYhxIriK2NyM2KpQMNFk1819LqNjK5gTWifoNONsCMFTuYcz8mW94sON_cgeJssQqaECeZlDbYcAfjinx-9Mg-9oYE-WjhqZ1410YONgd5AaIyOnnVeFYC6rl5-nr0EgCKKUOzqNLRjb8sFoNnNmldKxFxRLd313N4-hk852_vbdJEQPTMhattwkepMtmI9HP630rEWh1eiThe7HVnDHJ8HYCAdiFP3dj3_UUALThHhuUWnuEqeBRy7W6UXFrfIDJZHwLAeIEWw4cvVK0yvHKbv4hfC7WfrI0d8zw2bXuAHsqEwx-PBsKWVCby7fFbDB1t3WkW9lCk7ogeUmeJk7oNrmbQ1BNza0U3Rf5ItbWD3iDIaDlPnJGHhgPXJG77C116U4FMkiYHqHYzEz4mTF6nVI0-fyRZ_0omQ8zA4rVtX3aAjE1WgffIaQ7g2BbufaFvwgxNO6N3dY9s6IxKeUm22KPwaUI9t9XFBu2LtOWE8tqU_p8aiW47bOGdD5L2B3ji4BzmvkNkyIJkr2FiXh0YYrySLr6ZLCFBirt61wKeNKE=w572-h612-no)

**저장하기** 버튼을 누르는 것으로 가능합니다.

## 앞으로의 개발 사항
The purpose of this project is 
1. analyze Korean light novel publishing market.
2. auto-generate genre to light novels.
3. clustering based on genre, description, title, author, etc.

**The FINAL PURPOSE: light novel recommendation**
