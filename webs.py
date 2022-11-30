import time
from base64 import b64encode
from random import randint
from requests import get, packages
import json

packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"


def get_live_room():
    live_info = {}
    live_count = 0
    for i in range(1, 36):
        headers = get_header()
        province = str(i).zfill(2)
        url = f"https://xbk.189.cn/xbkapi/lteration/index/recommend/anchorRecommend?provinceCode={province}"
        data = get(url, headers=headers).json()
        if not data['data']:
            time.sleep(3)
            continue
        for live in data['data']:
            s = 1
            for info in live_info.values():
                if live == info:
                    s = 0
                    break
            if s:
                live_count += 1
                print(live_count)
                print(live)
                live_info[f"liveRoom{live_count}"] = live
        time.sleep(3)
    live_json = json.dumps(live_info, ensure_ascii=False)
    return live_json


def get_header():
    random_phone = f"1537266{randint(1000, 9999)}"
    headers = {
        "referer": "https://xbk.189.cn/xbk/newHome?version=9.4.0&yjz=no&l=card&longitude=%24longitude%24&latitude=%24latitude%24&utm_ch=hg_app&utm_sch=hg_sh_shdbcdl&utm_as=xbk_tj&loginType=1",
        "user-agent": f"CtClient;9.6.1;Android;12;SM-G9860;{b64encode(random_phone[5:11].encode()).decode().strip('=+')}!#!{b64encode(random_phone[0:5].encode()).decode().strip('=+')}"
    }
    return headers


def readfile():
    with open('xxx.json', 'r+', encoding='utf-8') as f:
        file_data = f.read()
    return file_data


def writefile(write_str):
    with open('xxx.json', 'w+', encoding='utf-8') as f:
        f.write(write_str)


def main():
    live_json = get_live_room()
    file_data = readfile()
    if live_json == file_data:
        print('直播间信息未变更，本次不做更新')
        return
    writefile(live_json)
    print('更新直播间信息完成')


if __name__ == '__main__':
    main()
