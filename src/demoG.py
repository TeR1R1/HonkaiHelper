import logging
import numpy as np
import models.utils.gameOCR as aocr
from paddleocr import PaddleOCR, draw_ocr
from airtest.aircv.aircv import *
from airtest.aircv.template_matching import *
from PIL import ImageGrab, ImageShow, Image

def ocrTest(image):
    ocr = PaddleOCR(
        use_angle_cls=True,
        show_log=False,
        lang="ch"
    )
    
    result = ocr.ocr(image, cls=True)

    result = result[0]
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    
    image = draw_ocr(image, boxes)
    image = Image.fromarray(image)
    
    for i in txts:
        print(i)
    image.show()
    
def imTest(im_source, im_search: list, rgb: bool=False):
    '''
    记得 im_search 要是一个列表！！！
    '''
    im_source_np = np.array(im_source)
    for i in range(len(im_search)):
        im_search_np = np.array(im_search[i])

        matcher = TemplateMatching(
            im_search=im_search_np,
            im_source=im_source_np,
            rgb=rgb
        )
        matcher.threshold = 0.8

        res = matcher.find_all_results()

        if not res is None:
            for x in res:
                mask_image(
                    img=im_source_np,
                    mask=x['rectangle'][0] + x['rectangle'][2],
                    color=(255, 0, 0),
                    linewidth=5
                )
    
    im_source = Image.fromarray(im_source_np)
    im_source.show()
    
if __name__ == '__main__':
    # 调整 'airtest' 的日志等级
    logger = logging.getLogger("airtest")
    logger.setLevel(logging.ERROR)
    
    honkai3 = aocr.getTitleNumber('崩坏3')
    aocr.setActive(honkai3)
    
    im_path = 'src/data/imdata/家园/'
    im_name = ['打工_S.png', '打工_A.png', '打工_C.png']
    
    im_s = (
        Image.open(im_path + im_name[0]),
        Image.open(im_path + im_name[1]),
        Image.open(im_path + im_name[2])
    )

    # image = aocr.getScreenshot(honkai3)
    # image = np.array(aocr.getScrPart((561, 35, 677, 75)))
    image = Image.open('tmp/demo.png')
    imTest(
        im_source=image,
        im_search=im_s
    )
    
    
    
    
