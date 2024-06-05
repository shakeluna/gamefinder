import streamlit as st
import requests
import pandas as pd
import datetime
import time
import re

def get_app_data(appid):
    try:
        appid = int(appid)
    except ValueError:
        return None
    
    if 1 <= appid <= 300000:
        table_name = "steamappid1"
    elif 300001 <= appid <= 600000:
        table_name = "steamappid2"
    elif 600001 <= appid <= 900000:
        table_name = "steamappid3"
    elif 900001 <= appid <= 1200000:
        table_name = "steamappid4"
    elif 1200001 <= appid <= 1500000:
        table_name = "steamappid5"
    elif 1500001 <= appid <= 1800000:
        table_name = "steamappid6"
    elif 1800001 <= appid <= 2100000:
        table_name = "steamappid7"
    elif 2100001 <= appid <= 2400000:
        table_name = "steamappid8"
    elif 2400001 <= appid <= 2700000:
        table_name = "steamappid9"
    elif 2700001 <= appid <= 3000000:
        table_name = "steamappid10"
    else:
        return None

    steam_api_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=kr"
    steam_response = requests.get(steam_api_url).json()
    game = steam_response[str(appid)]['data']['name']
    price = steam_response[str(appid)]['data']['price_overview']['final_formatted']
    steamappid = appid
    appidstr = str(appid)
    link = f"https://store.steampowered.com/app/{appidstr}/?l=koreana"
    price = int(re.sub(r'[^0-9]', '', price))
    original_price = price
    store = "스팀"
    new_row = pd.DataFrame({
        'store': [store],
        'game': [game],
        'steamappid': [steamappid],
        'original_price': [original_price],
        'price': [price],
        'link': [link],
    })

    url = "https://zsslzoptwfunhkrplsbv.supabase.co"
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpzc2x6b3B0d2Z1bmhrcnBsc2J2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQyODU3NDQsImV4cCI6MjAyOTg2MTc0NH0.6-QnGWhnY2ZshI6B2TPXReZNKyVLWJhyC0W9BwbviAM"
    endpoint = f"{url}/rest/v1/{table_name}"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}"
    }
    params = {
        "steamappid": f"eq.{appid}"
    }
    response = requests.get(endpoint, headers=headers, params=params)    
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            print("Query results:")
            for row in data:
                print(row)
        else:
            print("No matching records found for appid:", appid)
    else:
        print("Error occurred:", response.status_code, response.text)

    if data:
        df = pd.DataFrame(data)
        df = df.drop(columns=['id', 'range_label'])
        df = pd.concat([new_row, df], ignore_index=True)
        
        # Check if the required columns are present
        required_columns = ['game', 'store', 'price', 'link']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Missing columns: {missing_columns}")
            return None
        
        return df.assign(price=pd.to_numeric(df['price'], errors='coerce')).dropna(subset=['price']).sort_values(by='price', ascending=True)
    return None

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

    html += '<thead><tr><th>이름</th><th>유통사</th><th>가격(수수료불포함)</th><th>구매하러가기</th></tr></thead>'
    html += '<tbody>'
    
    for index, row in df.iterrows():
        # Formatting the price with commas
        formatted_price = f"{row['price']:,.0f} 원"
        html += f'<tr><td>{row["game"]}</td><td>{row["store"]}</td><td>{formatted_price}</td><td><a href="{row["link"]}">구매하러가기</a></td></tr>'
        
    html += '</tbody></table>'
    return html

url = st.text_input("원하는 스팀 게임 주소를 입력하고 스팀 게임 최저가 검색 버튼을 누르세요. 스크롤을 내려 사용방법을 확인하실 수 있습니다.")

if st.button("스팀 게임 최저가 검색"):
    with st.spinner('스팀 게임 최저가 검색 중'):
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
            game, store, price, link = first_row['game'], first_row['store'], first_row['price'], first_row['link']
            steam_price = fetch_steam_price(appid)

            # Check if price is a numerical value
            if isinstance(price, (int, float)):
                formatted_price = "{:,.0f} 원".format(float(price))
            else:
                formatted_price = "가격 정보 없음"
            
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
                                    <div><strong>상품 이름:</strong> {game}</div>
                                    <div><strong>상품 구매 사이트:</strong> {store}</div>
                                    <div><strong>상품 구매 최저가(수수료 불포함):</strong> {formatted_price}</div>
                                    <a href="{link}">구매하기</a>
                                """
                            
            # Generate the HTML table using the app_data DataFrame
            table_html = generate_html_table(app_data)
            
            # Combine the markdown content and the table HTML
            final_content = f"{table_html}"
            
            st.markdown("### 각 스토어 가격 정보")
            st.markdown(final_content, unsafe_allow_html=True)
                    
        else:
            st.write("해당 게임을 찾을 수 없습니다. 디럭스 에디션 등 다양한 에디션은 찾는데 제한이 있을 수 있습니다.")
        
        # Complete the progress bar when process is done
        progress_bar.progress(100)
