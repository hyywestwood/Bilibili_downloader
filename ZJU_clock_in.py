import requests, re

def _rsa_encrypt(self, password_str, e_str, M_str):
        password_bytes = bytes(password_str, 'ascii')
        password_int = int.from_bytes(password_bytes, 'big')
        e_int = int(e_str, 16)
        M_int = int(M_str, 16)
        result_int = pow(password_int, e_int, M_int)
        return hex(result_int)[2:].rjust(128, '0')

if __name__ == '__main__': 
    # 自动打卡分为三个步骤：1. 获取缓存的打卡信息； 2.构造提交信息 3. 提交信息
    username = '21834080'
    password = '5896westwood'
    # 登录打卡网址的url，登录成功后会自动跳转至打卡界面
    login_url = "https://zjuam.zju.edu.cn/cas/login?service=https%3A%2F%2Fhealthreport.zju.edu.cn%2Fa_zju%2Fapi%2Fsso%2Findex%3Fredirect%3Dhttps%253A%252F%252Fhealthreport.zju.edu.cn%252Fncov%252Fwap%252Fdefault%252Findex"
    
    base_url = "https://healthreport.zju.edu.cn/ncov/wap/default/index"
    save_url = "https://healthreport.zju.edu.cn/ncov/wap/default/save"
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }
    sess = requests.Session() # 开启会话，这样可以保持登录状态

    res = sess.get(login_url, headers = headers)
    execution = re.search('name="execution" value="(.*?)"', res.text).group(1)
    res = sess.get(url='https://zjuam.zju.edu.cn/cas/v2/getPubKey', headers=headers).json()
    n, e = res['modulus'], res['exponent']
    encrypt_password = _rsa_encrypt(password, e, n)
    data = {
            'username': username,
            'password': encrypt_password,
            'execution': execution,
            '_eventId': 'submit'
        }
    
    res = sess.post(url=login_url, data=data, headers=headers)

    # check if login successfully
    if '统一身份认证' in res.content.decode():
        raise LoginError('登录失败，请核实账号密码重新登录')
    # return sess
