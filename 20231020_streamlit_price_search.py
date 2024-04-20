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
        url = f"https://script.google.com/macros/s/AKfycbyIQNRS86_ZPmlsWO5wr9g1-E23UlL5zxyF4OG6hd6uQheJqsc_QcCeElT8RtIg1YQ5Nw/exec?steam_appid={appid}"
    elif 300001 <= appid <= 600000:
        url = f"https://script.google.com/macros/s/AKfycbz2uUQJXoqzgP6JBECwBsfiXG4bIaMsr6HAgbosC_ySbb4-9i8N-6C8lA7jdUnWVeAO/exec?steam_appid={appid}"
    elif 600001 <= appid <= 900000:
        url = f"https://script.google.com/macros/s/AKfycbxSvF4g3iCIchM5whNjTzvasFIH8KLj7IcmEY692pwVYmVTDKFZbknZfPNteOO8zsZGdw/exec?steam_appid={appid}"
    elif 900001 <= appid <= 1200000:
        url = f"https://script.google.com/macros/s/AKfycbwo1hWUsBnJBZV-sT9aa3BXSLs0G9Gql8480aX75mmKGzVRnrY5mAGZ9ZlUHH9kBQKrzg/exec?steam_appid={appid}"
    elif 1200001 <= appid <= 1500000:
        url = f"https://script.google.com/macros/s/AKfycbwkHOiqzJoveMTZcgfRy-_bJb-aSB65gjlTXt9LeHlDNbXmTzLIeb_R1CQfqsoGM_kY3w/exec?steam_appid={appid}"
    elif 1500001 <= appid <= 1800000:
        url = f"https://script.google.com/macros/s/AKfycbxlXrtBiO8dr7kIOu26QNj7oPDYZYPONqyCdWXodAkcFlHcouwAGrF-t0JYejDEI7jz/exec?steam_appid={appid}"
    elif 1800001 <= appid <= 2100000:
        url = f"https://script.google.com/macros/s/AKfycbxMwmSY1V7ippEiYYsdxUJgG5-3qFgBgNw4C8wxU0m7OnYs_VR_rhcREqtuIG__rsBV/exec?steam_appid={appid}"
    elif 2100001 <= appid <= 2400000:
        url = f"https://script.google.com/macros/s/AKfycbw5tafPV6Irz14D9SWUp988Oqxi5G7DR-W2nHP2EbPmc8X9Q-F7CtW0Z7CjHYjeGAeF/exec?steam_appid={appid}"
    elif 2400001 <= appid <= 2700000:
        url = f"https://script.google.com/macros/s/AKfycbyloLrn8cOIQSTRbuODb2OUnXE_Dc143LBl4CSFx_I6L4DGK9auM_vNTCrL7Jo7sdvs/exec?steam_appid={appid}"
    elif 2700001 <= appid <= 3000000:
        url = f"https://script.google.com/macros/s/AKfycbx2uB6sGx2Je0UTdJsRe_5ktQP88Z6L5ZrGYgA5SASfj3JoiaEePk_5etfH0PyLAPKA/exec?steam_appid={appid}"
    else:
        return None

    steam_api_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=kr"
    steam_response = requests.get(steam_api_url).json()
    game = steam_response[str(appid)]['data']['name']
    price = steam_response[str(appid)]['data']['price_overview']['final_formatted']
    steamapp_id = appid
    appidstr = str(appid)
    link = f"https://store.steampowered.com/app/{appidstr}/?l=koreana"
    price = int(re.sub(r'[^0-9]', '', price))
    original_price = price
    store = "스팀"

    new_row = pd.DataFrame({
    'name': [game],
    'steam_appid': [steamapp_id],
    'link': [link],
    'price': [price],
    'store': [store],
    'original_price': [original_price]
})
    
    
    response = requests.get(url)
    if response.status_code == 200:
        api_data = response.json()['data']
        if api_data:
            df = pd.DataFrame(api_data)
            df = pd.concat([new_row, df], ignore_index=True)            
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

    html += '<thead><tr><th>이름</th><th>구매사이트</th><th>구매가격(수수료 불포함)</th><th>유통사 이동</th></tr></thead>'
    html += '<tbody>'
    
    for index, row in df.iterrows():
        # Formatting the price with commas
        formatted_price = f"{row['price']:,.0f} 원"
        html += f'<tr><td>{row["name"]}</td><td>{row["store"]}</td><td>{formatted_price}</td><td><a href="{row["link"]}">구매하기</a></td></tr>'
        
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
            name, store, price, link = first_row['name'], first_row['store'], first_row['price'], first_row['link']
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
                                    <div><strong>상품 이름:</strong> {name}</div>
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
