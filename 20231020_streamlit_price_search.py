import streamlit as st
import requests
from requests.auth import HTTPBasicAuth


st.title('스팀 게임 최저가 정보 제공 사이트')
st.write('국내 외 다양한 사이트를 검색하여 스팀게임 최저가를 찾는 서비스입니다.')
st.write('저희 사이트는 프로토타입 프로젝트로 Streamlit을 통해 웹사이트를 운영하고 있습니다.')
st.write('Streamlit은 데이터 과학자와 엔지니어를 위한 빠르고 쉬운 웹 앱을 만들 수 있는 오픈소스 Python 라이브러리입니다.')
st.write('이상한 웹사이트가 아니라 전 세계에서 다양한 파이썬사용자들이 활용하는 웹사이트로 안전상의 이슈는 없습니다.')
st.write('만약 사용전에 의심이 되신다면 직접 streamlit에 대해서 검색해보시기 바랍니다.')


def get_app_data(appid):
    auth = HTTPBasicAuth('useradmin', 'awnetientoai11')
    response = requests.get("https://api.sheety.co/b642dc78968e02f9dd7ec2c1ad72493b/loweststoreonly/forDb", auth=auth)
    data = response.json()['forDb']
    
    for row in data:
        if str(row['steamAppid']) == str(appid):
            return row['name'], row['store'], row['price'], row['link']
    return None

def fetch_steam_price(appid):
    steam_api_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=kr"
    steam_response = requests.get(steam_api_url).json()
    if steam_response[str(appid)]['success']:
        return steam_response[str(appid)]['data']['price_overview']['final_formatted']
    return "가격 정보 없음"

url = st.text_input("스팀 주소를 입력하세요")

if st.button("검색"):
    appid = url.split("/app/")[1].split("/")[0]
    app_data = get_app_data(appid)
    
    if app_data:
        name, store, price, link = app_data
        st.write(f"상품 이름: {name}")
        st.write(f"상품 구매 사이트: {store}")
        st.write(f"상품 구매 가격(수수료 불포함): {price} 원")
        st.write(f"상품 구매 링크: {link}")
        st.image(f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg")
        
        steam_price = fetch_steam_price(appid)
        st.write(f"현재 스팀 가격: {steam_price} 원")
    else:
        st.write("해당 게임을 찾을 수 없습니다. 디럭스 에디션 등 다양한 에디션은 찾는데 제한이 있을 수 있습니다.")
