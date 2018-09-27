# !/usr/bin/env python
import os

from google.cloud import vision
from google.cloud.vision import types


class GoogleAPI:
    def __init__(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.path.dirname(__file__), 'MyFirstProject-8ca6b10b9659.json')

        self.client = vision.ImageAnnotatorClient()

    def detect_text(self, image_file):
        image = types.Image(content=image_file)
        # Performs label detection on the image file
        response = self.client.text_detection(image=image)
        labels = response.text_annotations
        if labels:
            return labels[0].description.strip()
        else:
            return


if __name__ == '__main__':
    # The name of the image file to annotate
    print(os.path.join(os.path.dirname(__file__),'MyFirstProject-8ca6b10b9659.json'))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.path.dirname(__file__), 'MyFirstProject-8ca6b10b9659.json')
    file_name = os.path.join(
        os.path.dirname(__file__),
        'text-detection-ctpn/data/demo/0_0.jpg')
    google_api = GoogleAPI()
    google_api.detect_text(file_name)
