import numpy as np
from datetime import datetime
import pandas as pd

# 1. 매개변수는 1개(데이터프레임)
def bnh(df, column, start, end) :
    # 인덱스 시계열로 변경
    df.index = pd.to_datetime(df.index)
    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    df = df.loc[start : end]
    # 2. 결측치, 무한대를 제거    
    df = df.loc[~df.isin([np.nan, np.inf, -np.inf]).any(1)]
    # 3. 수정종가만 있는 데이터프레임으로 변경
    df = df[[column]]
    # 4. 일별 수익율 파생변수 생성
    df["daily_rtn"] = df[column].pct_change()
    # 5. 누적 수익율 파생변수 생성
    df["st_rtn"] = (1 + df["daily_rtn"]).cumprod()
    # 6. 데이터프레임을 리턴
    return df