import streamlit as st
import requests
import pandas as pd
import datetime
import time

def get_app_data(appid):
    response = requests.get(f"https://script.google.com/macros/s/AKfycbxFgD6gzGca_NXW7k-oHXRV1OPfmqaWzj9PA_WT8S8CTvKboHUM8-NhwVPGvF2g-qwR/exec?steam_appid={appid}")
    data = response.json()['data']
    
    if data:
        df = pd.DataFrame(data)
        return df.sort_values(by='price', ascending=True)

def fetch_steam_price(appid):
    steam_api_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=kr"
    steam_response = requests.get(steam_api_url).json()
    try:
        if steam_response[str(appid)]['success']:
            return steam_response[str(appid)]['data']['price_overview']['final_formatted']
    except:
        return "스팀 가격 정보 확인 불가"
    return "가격 정보 없음"

def log_search_to_sheet(queried_url):
    url = 'https://script.google.com/macros/s/AKfycbxjZkbFucdlizWq_ivc26nijKHx7s9dIs9-ywHjNTCAy2y72hEoZW9N-3sQ772Fwi7u/exec'
    data = {'queriedUrl': queried_url}
    response = requests.post(url, json=data)

def generate_html_table(df):
    # Adding enhanced inline CSS for responsive table styling
    html = '''
    <style>
        .responsive-table {
            width: 100%;
            border-collapse: collapse;
        }
        .responsive-table th, 
        .responsive-table td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }
        .responsive-table th {
            background-color: #f2f2f2;
            font-size: 0.9em; /* Smaller font size for headers */
        }
        .responsive-table td {
            font-size: 0.8em; /* Smaller font size for data */
        }
        .responsive-table tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .responsive-table a:link,
        .responsive-table a:visited {
            color: #007bff; /* Bootstrap primary color for links */
            text-decoration: none;
        }
        .responsive-table a:hover,
        .responsive-table a:active {
            text-decoration: underline;
        }
    </style>
    <table class="responsive-table">
    '''

    html += '<thead><tr><th>상품 이름</th><th>상품 구매 사이트</th><th>상품 구매 가격(수수료 불포함)</th><th>상품 구매 링크</th></tr></thead>'
    html += '<tbody>'
    
    for index, row in df.iterrows():
        # Formatting the price with commas
        formatted_price = f"{row['price']:,.0f} 원"
        html += f'<tr><td>{row["name"]}</td><td>{row["store"]}</td><td>{formatted_price}</td><td><a href="{row["link"]}">구매하기</a></td></tr>'
        
    html += '</tbody></table>'
    return html

url = st.text_input("스팀 주소를 입력하세요")

if st.button("검색"):
    with st.spinner('Processing...'):
        progress_bar = st.progress(0)
        
        # Simulate process update
        for i in range(100):
            # Update progress bar with each iteration.
            progress_bar.progress(i+1)
            time.sleep(0.01)  # Simulate processing time
        appid = url.split("/app/")[1].split("/")[0]
        app_data = get_app_data(appid)
        queried_url = f"https://store.steampowered.com/app/{appid}/"
        log_search_to_sheet(queried_url)
        
        if app_data is not None and not app_data.empty:
            first_row = app_data.iloc[0]
            name, store, price, link = first_row['name'], first_row['store'], first_row['price'], first_row['link']
            steam_price = fetch_steam_price(appid)

            # Format the price with commas
            formatted_price = f"{price:,.0f} 원"
            
            markdown_content = f"""
                                    <style>
                                        table {{
                                            width: 100%;
                                            border-collapse: collapse;
                                        }}
                                        th, td {{
                                            text-align: left;
                                            padding: 8px;
                                            border-bottom: 1px solid #ddd;
                                        }}
                                        th {{
                                            background-color: #f2f2f2;
                                        }}
                                        img.game-image {{
                                            max-width: 100%;
                                            height: auto;
                                            display: block;
                                            margin-left: auto;
                                            margin-right: auto;
                                        }}
                                    </style>
                                    <img src="https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg" class="game-image">
                                    <div><strong>현재 스팀 가격:</strong> {steam_price}</div>
                                    <div><strong>상품 이름:</strong> {name}</div>
                                    <div><strong>상품 구매 사이트:</strong> {store}</div>
                                    <div><strong>상품 구매 최저가(수수료 불포함):</strong> {formatted_price}</div>
                                    <a href="{link}">구매하기</a>
                                """
    
            # Use Markdown for better formatting and apply inline CSS for styling
            
            st.markdown("### 최저가 사이트 외 사이트 정보")
            st.markdown(markdown_content, unsafe_allow_html=True)
            
        else:
            st.write("해당 게임을 찾을 수 없습니다. 디럭스 에디션 등 다양한 에디션은 찾는데 제한이 있을 수 있습니다.")
        
        # Complete the progress bar when process is done
        progress_bar.progress(100)
