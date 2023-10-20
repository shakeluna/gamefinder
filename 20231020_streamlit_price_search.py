import streamlit as st
import requests

st.title('스팀 앱 정보')
st.write('저희 사이트는 프로토타입 프로젝트로 Streamlit을 통해 웹사이트를 운영하고 있습니다.')

def get_app_data(appid):
    response = requests.get(f"https://api.sheety.co/b642dc78968e02f9dd7ec2c1ad72493b/loweststoreonly/forDb")
    data = response.json()['forDb']
    
    for row in data:
        if row['steamAppid'] == int(appid):
            return row['name'], row['store'], row['price'], row['link']
    return None

def fetch_steam_price(appid):
    steam_api_url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    steam_response = requests.get(steam_api_url).json()
    if steam_response[str(appid)]['success']:
        return steam_response[str(appid)]['data']['price_overview']['final_formatted']
    return "가격 정보 없음"

url = st.text_input("스팀 URL을 입력하세요")

if st.button("검색"):
    appid = url.split("/app/")[1].split("/")[0]
    app_data = get_app_data(appid)
    
    if app_data:
        name, store, price, link = app_data
        st.write(f"이름: {name}")
        st.write(f"상점: {store}")
        st.write(f"가격: {price}")
        st.write(f"링크: {link}")
        st.image(f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg")
        
        steam_price = fetch_steam_price(appid)
        st.write(f"스팀 가격: {steam_price}")
    else:
        st.write("찾을 수 없습니다.")
