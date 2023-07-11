# เป็นสคริปส์ตัวอย่างการใช้ requests ทำงานตัว api ไม่เกี่ยวกับ src code bot

import requests

def tmweasy_api(username, password, tmemail, action, transactionid, clientip, ref1, json):
    base_url = "https://www.tmweasy.com/apiwallet.php"

    url = f"{base_url}?username={username}&password={password}&tmemail={tmemail}&action={action}&transactionid={transactionid}&clientip={clientip}&ref1={ref1}&json={json}"

    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        return None

username = "" # --> user ของ tmweasy
password = "" # --> pass ของ tmweasy
tmemail = ""  # --> เบอร์โทรศัพท์
action = "yes"
transactionid = "" # --> ซองอังเปา
clientip = "" # --> ip 
ref1 = "" # --> user ของ tmweasy
json = "1"

response = tmweasy_api(username, password, tmemail, action, transactionid, clientip, ref1, json)
if response is not None:
    status = response.get('Status')
    money = response.get('Amount')
    if status == 'check_success':
        print(f"คุณได้เติมเงินสำเร็จเเล้วจำนวน {money} บาท")
    else:
        print("ซองอังเปาไม่ถูกต้อง")
else:
    print("Request failed.")
