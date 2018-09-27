import requests
import json
import base64
from io import BytesIO
# pip3 install pillow
from PIL import Image


class BaiDuOCR:
    def __init__(self, client_id, client_secret):
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'\
            .format(client_id, client_secret)
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        response = requests.get(host, headers=headers)
        content = response.content
        self.access_token = ''
        if content:
            content_json = json.loads(content.decode())
            self.access_token = content_json['access_token']
        else:
            raise Exception('未获取access_token')

    def image_to_base64(self, image_path):
        img = Image.open(image_path)
        output_buffer = BytesIO()
        img.save(output_buffer, format='JPEG', quality=100)
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data)
        return base64_str

    def general_basic(self, image_base64):
        post_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
        post_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = dict()
        payload['access_token'] = self.access_token
        payload['image'] = image_base64.decode()
        payload['language_type'] = 'CHN_ENG'
        payload['detect_direction'] = 'false'
        payload['detect_language'] = 'false'
        payload['probability'] = 'true'
        r = requests.post(post_url, headers=post_headers, data=payload)
        return r.json()


if __name__ == '__main__':
    _image = "/home/sun/duola/text-detection-ctpn/data/cutpic/0_5.jpg"
    AK, SK = 'Yzzftrmi2Z6mGGy8nqsg8DQc', 'LagFcm3I0632r9ZeZEcn7z0d271KMM9y'
    baidu_ocr = BaiDuOCR(AK, SK)
    result = baidu_ocr.general_basic(baidu_ocr.image_to_base64(_image))
    print(result)
