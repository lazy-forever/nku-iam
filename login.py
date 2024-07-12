from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests
import json

iam_url = "https://iam.nankai.edu.cn/"

def encrypt(password):
    key = "8bfa9ad090fbbf87e518f1ce24a93eee".encode('utf-8')
    iv = "fbfae671950f423b58d49b91ff6a22b9".encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv[:16])
    encrypted_hex = cipher.encrypt(pad(password.encode('utf-8'), AES.block_size)).hex()
    return encrypted_hex

def test_login(username, password):
    encrypted_password = encrypt(password)
    print("test login")
    loginurl = iam_url + "api/v1/login?os=web"
    headers = {
        "Content-Type": "application/json"
    }
    data = {"login_scene":"feilian","account_type":"userid","account":username,"password":encrypted_password}
    try:
        response = requests.post(loginurl, headers=headers, data=json.dumps(data))
    except Exception as e:
        print("network error:"+str(e))
        return False
    '''
    right_response = {"code":0,"action":"","message":"","data":{"result":"success","next":{"action":"GoToLink","can_skip":true}}}
    wrong_response = {"code":10110001,"action":"alert","message":"用户名或密码错误，请再次输入，如确认无误可联系管理员排查。(10110001)"}
    '''
    response = response.json()
    print(response)
    if response["code"] == 0:
        print("login success")
        return True
    else:
        print("login failed:"+response["message"])
        return False
    


if __name__ == "__main__":
    # print(encrypt("aa'\\"))
    test_login("username", "password")
    