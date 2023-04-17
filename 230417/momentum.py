import pandas as pd
import numpy as np
from datetime import datetime


# 1. 첫번째 함수
# 매개변수 1게(데이터프레임)
def mmt1 (df, col = "Close", start = "20100101", end = "20230101") :
    # 인덱스가 Date가 아니면? Date 컬럼을 인덱스로 변경
    if "Date" in df.columns :
        df = df.set_index("Date")
    # start, end를 시계열로 변경
    start = datetime.strptime(start, "%Y%m%d").isoformat()
    end = datetime.strptime(end, "%Y%m%d").isoformat()
    # 데이터프레임에 결측치와 이상치를 제거, 수정종가를 제외한 나머지 컬럼은 삭제
    df = df.loc[~df.isin([np.nan, np.inf, -np.inf]).any(1), [col]]
    # 인덱스를 시계열로 변경
    df.index = pd.to_datetime(df.index, format = "%Y-%m-%d")
    df = df.loc[start : end]
    # "STD-YM" 파생변수를 생성하여 인덱스의 년-월 추출해서 대입
    df["STD-YM"] = list(map(lambda x : datetime.strftime(x, "%Y-%m"), df.index))
    return df


# 2. 두번째 함수
# 매개변수 1개(데이터프레임)
def mmt2 (df) :
    col = df.columns[0]
    # 새로운 데이터프레임 생성
    df2 = pd.DataFrame()
    # 인자값으로 받아온 데이터프레임에서 년-월별 마지막 데이터들을 새로운 데이터프레임에 대입
    df2 = df.loc[df["STD-YM"] != df.shift(-1)["STD-YM"]]
    # df에 파생변수 2개 생성
    # "BF_1M" : 전월의 종가, 결측치는 0으로 대체
    df2["BF_1M"] = df2.shift(1)[col].fillna(0)
    # "BF_12M" : 전년도의 종가, 결측치는 0으로 대체
    df2["BF_12M"] = df2.shift(12)[col].fillna(0)
    return df2
    

# 3. 세번째 함수
# 매개변수 2개(첫번째 함수의 결과(df1), 두번째 함수의 결과(df2))
def mmt3(df1, df2) :
    # df1에 trade 컬럼을 생성, 값은 ""
    df1["trade"] = ""
    # df1에 return 컬럼을 생성, 값은 1
    df1["return"] = 1
    col = df1.columns[0]
    # df2의 값들을 이용하여 momentum_index를 구하고 df1에 거래 내역 삽입
    for i in df2.index :
        signal = ""
        # 절대 모멘텀 계산
        momentum_index = df2.loc[i, "BF_1M"] / df2.loc[i, "BF_12M"] - 1
        # 절대 모멘텀 지표에 따라서 True 와 False 로 구분
        flag = True if((momentum_index > 0) and (momentum_index != -np.inf) and(momentum_index != np.inf)) else False
        if flag :
            signal = "buy"
        df1.loc[i, "trade"] = signal
    # df1의 거래 내역을 이용하여 수익율 return 컬럼에 대입
    # 2. rtn = 1.0, buy, sell 변수는 0으로 생성
    rtn = 1.0 
    buy = 0
    sell = 0

    for i in df1.index :
        # 3. 반복문을 이용해서 현재의 trade가 buy이고 전 행의 trade가 "" 인 경우 구매 날
        if (df1.loc[i, "trade"] == "buy") and (df1.shift(1).loc[i, "trade"] == "") :
            buy = df1.loc[i, col]
            print("구입일 : ", i, "구입 가격 : ", buy)
        # 4. 전 행의 trade가 buy이고 현재의 trade가 "" 인 경우 판매 날
        elif (df1.shift(1).loc[i, "trade"] == "buy") and (df1.loc[i, "trade"] == "") :
            sell = df1.loc[i, col]
            # 5. 수익율 계산해서 return 대입
            print("판매일 : ", i, "판매가격 : ", sell)
            rtn = (sell - buy) / buy + 1
            df1.loc[i, "return"] = rtn
            
    # return 컬럼의 데이터를 가지고 누적수익율(acc_rtn)에 대입
    acc_rtn = 1.0
    for i in df1.index :
        acc_rtn *= df1.loc[i, "return"]
        df1.loc[i, "acc_rtn"] = acc_rtn
    print(acc_rtn)

    return df1

