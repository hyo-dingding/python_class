import pandas as pd
import warnings
import matplotlib.pyplot as plt
plt.rc('font', family='Malgun Gothic')
warnings.filterwarnings('ignore')


def get_exchange_rate_data(code) :
    df = pd.DataFrame()
    
    for page_num in range(1,11):
        base_url = f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{code}KRW&page={page_num}"
        tamp = pd.read_html(base_url, encoding='cp949', header=1)
        
        df = pd.concat([df, tamp[0]])
        
    total_rate_data_view(df)


def total_rate_data_view(df) :
    # 원하는 열만 추출
    df_total = df[['날짜', '매매기준율', '사실 때', '파실 때', '보내실 때', '받으실 때']]

    # 데이터 표시
    print(f'=========={currency_name[code_in]}-{code}==========')
    print(df_total.head(20))

    # 전체 차트작성
    df_total_chart = df_total.copy()
    df_total_chart = df_total_chart.set_index('날짜')

    # 최신데이터와 과거데이터의 순서를 바꿈. 역순으로 표시
    df_total_chart=df_total_chart[::-1]
    df_total_chart['매매기준율'].plot(figsize=(15, 6), title='Total exchange rate')
    plt.show()
    
    month_rate_data_view(df_total)



def month_rate_data_view(df_total) :
    # 월별 검색
    # 날짜 열 형변환(문자열 -> 날짜형식) 
    df_total['날짜']=df_total['날짜'].str.replace(".","").astype('datetime64[ms]')

    # '월' 파생변수 생성 
    df_total['월'] = df_total['날짜'].dt.month
    month_in = int(input('검색할 월 입력>>'))
    month_df = df_total.loc[df_total['월'] == month_in, ['날짜', '매매기준율', '사실 때','파실 때',	'보내실 때','받으실 때'	]]

    # 데이터 표시
    print(f'=========={currency_name[code_in]}-{code}==========')
    print(month_df.head(20))

    # 인덱스 재조정
    month_df = month_df.reset_index(drop=True)
    month_df_chart = month_df.copy()
    month_df_chart = month_df_chart.set_index('날짜')
    month_df_chart['매매기준율'].plot(figsize=(15,6))
    plt.show()


code_in = int(input('통합유형 선택(1:USD, 2:EUR, 3:JPY)'))
currency_symbols = ['USD', 'EUR', 'JPY']
currency_name = ['미국 달러', '유럽연합 유로', '일본 엔(100)']
code = currency_symbols[code_in-1]

get_exchange_rate_data(code)
