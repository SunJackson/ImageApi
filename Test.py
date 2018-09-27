# -*- coding: utf-8 -*-
from PIL import Image
import base64
from io import BytesIO
from BaiduAPI import BaiDuOCR
from GoogleAPI import GoogleAPI
import os


def get_file_names(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpeg' or os.path.splitext(file)[1] == '.jpg':
                L.append(os.path.splitext(file))
    return L

class TESTBAIDU:
    def __init__(self):
        AK, SK = 'Yzzftrmi2Z6mGGy8nqsg8DQc', 'LagFcm3I0632r9ZeZEcn7z0d271KMM9y'
        self.baidu_ocr = BaiDuOCR(AK, SK)

    # 其中os.path.splitext()函数将路径拆分为文件名+扩展名
    def rec_img(self, name):
        fw = open('/home/sun/duola/text-detection-ctpn/data/baidu_results/res_test.txt', 'a+')
        fr = open('/home/sun/duola/text-detection-ctpn/data/results/res_{}.txt'.format(name[0]), 'r')
        im = Image.open('/home/sun/duola/text-detection-ctpn/data/demo/{}'.format(''.join(name)))
        lines = fr.read().strip().split('\n')
        fr.close()
        # image_location_y, image_location_x = name[0].split('_')
        for line in lines:
            crops = line.split('\t')
            im2 = im.crop((int(crops[0]), int(crops[1]), int(crops[2]), int(crops[3])))
            output_buffer = BytesIO()
            im2.save(output_buffer, "JPEG", quality=100)
            byte_data = output_buffer.getvalue()
            base64_str = base64.b64encode(byte_data)
            result = self.baidu_ocr.general_basic(base64_str)
            words = []
            if 'words_result' in result:
                for words_result in result['words_result']:
                    words.append(words_result['words'].replace(';', '').replace('.', '').replace(',', ''))
                result_words = ';'.join(words)
                # crops[0] = str(int(crops[0]) + int(image_location_x)*800)
                # crops[1] = str(int(crops[1]) + int(image_location_y)*800)
                # crops[2] = str(int(crops[2]) + int(image_location_x)*800)
                # crops[3] = str(int(crops[3]) + int(image_location_y)*800)
                crops.append(result_words)
                if result_words:
                    fw.write('\t'.join(crops) + '\n')
            else:
                print(name, result)
        fw.close()

    def test_baidu_api(self):
        demo_path = '/home/sun/duola/text-detection-ctpn/data/demo/'
        file_names = get_file_names(demo_path)
        for file_name in file_names:
            self.rec_img(file_name)


class TESTGOOGLE:
    def __init__(self):
        self.google_api = GoogleAPI()

    # 其中os.path.splitext()函数将路径拆分为文件名+扩展名
    def rec_img(self, name):
        fw = open('/home/sun/duola/text-detection-ctpn/data/baidu_results/res_all_google.txt', 'a+')
        fr = open('/home/sun/duola/text-detection-ctpn/data/results/res_{}.txt'.format(name[0]), 'r')
        im = Image.open('/home/sun/duola/text-detection-ctpn/data/demo/{}'.format(''.join(name)))
        lines = fr.read().strip().split('\n')
        fr.close()
        image_location_y, image_location_x = name[0].split('_')
        for line in lines:
            crops = line.split('\t')
            im2 = im.crop((int(crops[0]), int(crops[1]), int(crops[2]), int(crops[3])))
            output_buffer = BytesIO()
            im2.save(output_buffer, "JPEG", quality=100)
            byte_data = output_buffer.getvalue()
            result = self.google_api.detect_text(byte_data)
            if result:
                result_words = ';'.join(result.split(' '))
                crops[0] = str(int(crops[0]) + int(image_location_x) * 800)
                crops[1] = str(int(crops[1]) + int(image_location_y) * 800)
                crops[2] = str(int(crops[2]) + int(image_location_x) * 800)
                crops[3] = str(int(crops[3]) + int(image_location_y) * 800)
                crops.append(result_words)
                if result_words:
                    fw.write('\t'.join(crops) + '\n')
            else:
                print(name, result)
        fw.close()

    def test_google_api(self):
        demo_path = '/home/sun/duola/text-detection-ctpn/data/demo/'
        file_names = get_file_names(demo_path)
        for file_name in file_names:
            self.rec_img(file_name)


if __name__ == '__main__':
    test_baidu = TESTBAIDU()
    test_baidu.test_baidu_api()
    # test_google = TESTGOOGLE()
    # test_google.test_google_api()

