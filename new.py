import time

a = time.time()

from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, use_gpu=False)  # 使用CPU预加载，不用GPU
img = r"C:\Users\BirchForest\Desktop\iQELAqNqcGcDAQTNCrAFzQ5ABtoAI4QBpCE18MICqiG_h3vjBvP1CFUDzwAAAYwGdCqdBM4A9_CxB84pWQqfCAAKBg.jpg_720x720q90.jpg"
text = ocr.ocr(img, cls=True)  # 打开图片文件
# 打印所有文本信息
print('\n'.join([i[1][0] for i in text[0]]))

print(time.time() - a)
