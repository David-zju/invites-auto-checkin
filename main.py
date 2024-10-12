import requests, re, json

with open("data.json", "r") as f:
    data = json.load(f)
cookies = data["cookies"]

def get_token(session):
    url = "https://invites.fun/"
    response = session.get(url, cookies=cookies)
    html_content = response.text
    csrf_token_pattern = r'"csrfToken":"([a-zA-Z0-9]+)"'
    user_id_pattern = r'"userId":([a-zA-Z0-9]+)'
    match1 = re.search(user_id_pattern, html_content)
    match2 = re.search(csrf_token_pattern, html_content)
    
    if match1 == None:
        print("ERROR: user id not found.")
        return None
    if match2:
        csrf_token = match2.group(1)
        user_id = match1.group(1)
        return csrf_token, user_id
    else:
        print("ERROR: CSRF Token not found.")
        return None

def sign_in_invites(session):
    csrf_token, user_id = get_token(session)
    # 请求的 URL
    check_in_url = "https://invites.fun/api/users/" + user_id

    # 请求头信息
    print("flarum_remember=" + cookies["flarum_remember"] + "; flarum_session=" + cookies["flarum_session"])
    headers = {
        "authority": "invites.fun",
        "method": "POST",
        "path": "/api/users/" + user_id,
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json; charset=UTF-8",
        "cookie": "flarum_remember=" + cookies["flarum_remember"] + "; flarum_session=" + cookies["flarum_session"], 
        "dnt": "1",
        "origin": "https://invites.fun",
        "referer": "https://invites.fun/",
        "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36",
        "x-csrf-token": csrf_token,
        "x-http-method-override": "PATCH"
    }

    # 请求体
    data = {
        "data": {
            "type": "users",
            "attributes": {
                "canCheckin": False,
                "totalContinuousCheckIn": 1
            },
            "id": user_id
        }
    }

    # 发送 POST 请求
    response = session.post(check_in_url, json=data, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应体
        result = response.json()
        
        # 检查 canCheckin 和 totalContinuousCheckIn 等字段
        can_checkin = result['data']['attributes'].get('canCheckin', None)
        total_checkins = result['data']['attributes'].get('totalContinuousCheckIn', None)
        money = result['data']['attributes'].get('money', None)  # 获取用户的money信息
        
        if can_checkin is False:
            print(f"💊签到成功，连续签到次数：{total_checkins}，药丸数量：{money}".format())
        else:
            print("签到失败或已经签到过了")
    else:
        print(f"请求失败，状态码: {response.status_code}")


if __name__ == "__main__":
    session = requests.Session()
    sign_in_invites(session)