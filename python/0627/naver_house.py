import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm # 한글폰트 설정을 위한 설치 
 
# 한글폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'
fontprop = fm.FontProperties(fname=font_path, size=12)
plt.rc('font', family=fontprop.get_name()) 
 
def collect_data(base_url, pages) :
    df_rates = pd.DataFrame() 
    for page_num in range(1,pages + 1) : 
        url = f"{base_url}?page={page_num}"
        data = pd.read_html(url)

        df = data[0]
        temp = df.copy()
        df_temp = temp['제목'].str.replace('%', "")

        regions = ['전국', '서울', '수도권']
        for region in regions:
            df_temp = df_temp.str.replace(region, "")

        df_temp = df_temp.str.split(']', expand=True)
        df_temp = df_temp[1].str.split(',', expand=True)
        df_temp = df_temp.astype(float)
        temp[regions] = df_temp

        df_rate = temp[['등록일'] + regions + ['번호']]
        df_rates = pd.concat([df_rates, df_rate])
        
    df_rates = df_rates[::-1]
        
    # '등록일' 열을 datetime 형식으로 변환
    # df_total_chart['등록일'] = df_total_chart['등록일'].str.replace(".","").astype('datetime64[ms]')
    df_rates['등록일'] = pd.to_datetime(df_rates['등록일'].str.replace(".", ""))
    print('데이터출력:',df_rates.info())
    return df_rates
    
    
 # 주별 데이터 조회
def plot_weekly_data(df_rates) : 
    df_rates.head(30).plot(x='등록일', y=['전국', '서울', '수도권'], figsize=(15,8))
    plt.title('주별 데이터 조회')
    plt.grid(True)
    plt.show()
    print(df_rates)


# 월별 추이 분석
def plot_monthly_data(df_rates) :
   df_total_chart = df_rates.copy()
   df_total_chart['월'] = df_total_chart['등록일'].dt.month
   
   month_avg = df_total_chart.groupby('월')[['전국', '서울', '수도권']].mean().reset_index() 
   month_avg.head(30).plot(x='월', y=['전국', '서울', '수도권'], figsize=(15,8))
   plt.title('월별 추이 분석')
   plt.grid(True)
   plt.show()
   print(month_avg)

   
# 년도별 추이 분석
def plot_yearly_data(df_rates) :
    df_total_chart = df_rates.copy()
    df_total_chart['연도'] = df_total_chart['등록일'].dt.year
    
    year_avg = df_total_chart.groupby('연도')[['전국', '서울', '수도권']].mean().reset_index()
    year_avg.head(20).plot(x='연도', y=['전국', '서울', '수도권'], figsize=(15,8))
    plt.title('연도별 추이 분석')
    plt.grid(True)
    plt.show()
    print(year_avg)
     


base_url = 'https://land.naver.com/news/trendReport.naver'

df_rates = collect_data(base_url, 10)
    
plot_weekly_data(df_rates)
plot_monthly_data(df_rates)
plot_yearly_data(df_rates)
    
