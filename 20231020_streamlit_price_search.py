import streamlit as st
import requests
import pandas as pd


st.title('스팀 게임 최저가 정보 제공 사이트')
st.write('국내 외 다양한 사이트를 검색하여 스팀게임 최저가를 찾는 서비스입니다.')
st.write('저희 사이트는 프로토타입 프로젝트로 Streamlit을 통해 웹사이트를 운영하고 있습니다.')
st.write('Streamlit은 데이터 과학자와 엔지니어를 위한 빠르고 쉬운 웹 앱을 만들 수 있는 오픈소스 Python 라이브러리입니다.')
st.write('이상한 웹사이트가 아니라 전 세계에서 다양한 파이썬사용자들이 활용하는 웹사이트로 안전상의 이슈는 없습니다.')
st.write('만약 사용전에 의심이 되신다면 직접 streamlit에 대해서 검색해보시기 바랍니다.')


def get_app_data(appid):
    response = requests.get(f"https://script.google.com/macros/s/AKfycbw5ci2n5IgXzn2HkEDvh4wr9_08TBys3KqUBoDroFN4NOQTc4qGhHmZr7xPAT3F9ltI/exec?steam_appid={appid}")
    data = response.json()['data']
    
    if data:
        df = pd.DataFrame(data)
        return df.sort_values(by='price', ascending=True)

def fetch_steam_price(appid):
    steam_api_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=kr"
    steam_response = requests.get(steam_api_url).json()
    if steam_response[str(appid)]['success']:
        return steam_response[str(appid)]['data']['price_overview']['final_formatted']
    return "가격 정보 없음"

def generate_html_table(df):
    # Adding some basic inline CSS for table styling
    html = '''
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
    </style>
    <table>
    '''

    html += '<thead><tr><th>상품 이름</th><th>상품 구매 사이트</th><th>상품 구매 가격(수수료 불포함)</th><th>상품 구매 링크</th></tr></thead>'
    html += '<tbody>'
    
    for index, row in df.iterrows():
        # Formatting the price with commas
        formatted_price = "{:,.0f} 원".format(row["price"])
        html += f'<tr><td>{row["name"]}</td><td>{row["store"]}</td><td>{formatted_price}</td><td><a href="{row["link"]}">구매하기</a></td></tr>'
        
    html += '</tbody></table>'
    return html


url = st.text_input("스팀 주소를 입력하세요")

if st.button("검색"):
    appid = url.split("/app/")[1].split("/")[0]
    app_data = get_app_data(appid)
    
    if app_data is not None and not app_data.empty:
        first_row = app_data.iloc[0]
        name, store, price, link = first_row['name'], first_row['store'], first_row['price'], first_row['link']
        steam_price = fetch_steam_price(appid)

        # Use Markdown for better formatting and apply inline CSS for styling
        st.markdown(f"""
    <style>
        .info {{
            font-size: 16px;
            margin-bottom: 5px;
        }}
        .info-title {{
            font-weight: bold;
            display: inline-block;
            width: 150px;
        }}
        .game-image {{
            width: 100%;
            height: auto;
            margin-bottom: 10px;
        }}
    </style>
    <div>
        <div class="info"><span class="info-title">현재 스팀 가격:</span> {steam_price} 원</div>
        <div class="info"><span class="info-title">상품 이름:</span> {name}</div>
        <div class="info"><span class="info-title">상품 구매 사이트:</span> {store}</div>
        <div class="info"><span class="info-title">상품 구매 가격(수수료 불포함):</span> {price:,.0f} 원</div>
        <a href="{link}"><div class="info buy-link">구매하기</div></a>
    </div>
    """, unsafe_allow_html=True)

        # Display game image
        st.image(f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg", use_column_width=True)

        st.markdown("### 최저가 사이트 외 사이트 정보")
        st.markdown(generate_html_table(app_data), unsafe_allow_html=True)
    else:
        st.write("해당 게임을 찾을 수 없습니다. 디럭스 에디션 등 다양한 에디션은 찾는데 제한이 있을 수 있습니다.")
