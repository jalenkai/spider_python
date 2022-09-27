import os
import pytesseract
from PIL import Image
from collections import defaultdict,namedtuple
#OCR，光學字元辨識(Optical Character Recognition) 意思是可以把照片中的文字轉化成文字檔
#絕對路徑 , lang="eng" pytesseract.image_to_string("IMAGE",lang="指定語言")
# tesseract.exe所在的文件路徑
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#OCR 辨識繁體中文


#擷取圖片中像素點數量最多的像素
def get_threshold(image):
    pixel_dict = defaultdict(int)
    # 像素及該像素出現次數的字典
    rows, cols = image.size
    for i in range(rows):
        for j in range(cols):
            pixel = image.getpixel((i, j))
            pixel_dict[pixel] += 1

    count_max = max(pixel_dict.values()) #擷取像素出現出多的次數
    pixel_dict_reverse = {v:k for k,v in pixel_dict.items()}
    threshold = pixel_dict_reverse[count_max] #擷取出現次數最多的像素點

    return threshold

# 按照圖值進行二值化處理
# threshold: 像素圖值
def get_bin_table(threshold):
    #擷取灰度轉二值的映射table
    table = []
    for i in range(256):
        rate = 0.1 #在threshold的適當範圍内進行處理
        if threshold*(1-rate)<= i <= threshold*(1+rate):
            table.append(1)
        else:
            table.append(0)
    return table

# 去掉二值化處理後的圖片中的噪聲點(圖像雜訊)
def cut_noise(image):

    rows, cols = image.size # 圖片的寬度和高度
    change_pos = [] # 紀錄噪聲點(圖像雜訊)位置

    # 邊緣圖片中的每個點，除掉邊緣
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            # pixel_set用來紀錄該點附近的黑色像素的數量
            pixel_set = []
            # 取該點的領域為以該點為中心的九宫格
            for m in range(i-1, i+2):
                for n in range(j-1, j+2):
                    if image.getpixel((m, n)) != 1: # 1為白色,0位黑色
                        pixel_set.append(image.getpixel((m, n)))

            # 如果該位置的九宫内的黑色數量小於等於4，則判斷為噪聲點(圖像雜訊)
            if len(pixel_set) <= 4:
                change_pos.append((i,j))

    # 對相對位置進行像素修改，將噪聲點(圖像雜訊)的像素置為1（白色）
    for pos in change_pos:
        image.putpixel(pos, 1)

    return image # 返回修改後的圖片

# 識別别圖片中的數字加字母
# 傳入参數為圖片路逕，返回結果為：識別結果
def OCR_lmj(img_path):
    image = Image.open(img_path) # 打開圖片文件
    imgry = image.convert('L')  # 轉化為灰度圖
    # 擷取圖片中的出現次數最多的像素，即為該圖片的背景
    max_pixel = get_threshold(imgry)

    #將圖片進行二值化處理
    table = get_bin_table(threshold=max_pixel)
    out = imgry.point(table, '1')

    # 去掉圖片中的噪聲點(圖像雜訊)（孤立點）
    out = cut_noise(out)

    #保存圖片
    # out.save('E://figures/img_gray.jpg')

    # 找尋識別圖片中的數字
    #text = pytesseract.image_to_string(out, config='digits')
    # 識別圖片中的數字和字母
    text = pytesseract.image_to_string(out,lang='chi_tra+eng')

    # 去掉識別結果中的特殊字符
    exclude_char_list = ' .:\\|\'\"?![],()~@#$%^&*_+-={};<>/¥'
    text = ''.join([x for x in text if x not in exclude_char_list])
    #print(text)

    return text

def main():

    # 識別指定文件目錄下的圖片
    # 圖片存放目錄figures
    dir = 'E://figures'

    correct_count = 0  # 圖片總數
    total_count = 0    # 識別正正確的圖片數量
    '''
    # 找尋figures下的png,jpg文件
    for file in os.listdir(dir):
        if file.endswith('.png') or file.endswith('.jpg'):
            # print(file)
            image_path = '%s/%s'%(dir,file) # 圖片路逕

            answer = file.split('.')[0]  # 圖片名稱，即圖片中的正確文字
            recognizition = OCR_lmj(image_path) # 圖片識別的文字結果

            print((answer, recognizition))
            if recognizition == answer: # 如果識別結果正確，則total_count加1
                correct_count += 1

            total_count += 1

    print('Total count: %d, correct: %d.'%(total_count, correct_count))
    
    '''
    # 單張圖片識別
    image_path = 'C:\MyProject\python\webspider\webspider\imgtemp\images2.jpeg'
    print(OCR_lmj(image_path))

#處理彩色的數字圖片
def convert_img(img,threshold):
    img = img.convert("L")  # 處理灰白
    pixels = img.load()
    for x in range(img.width):
        for y in range(img.height):
            if pixels[x, y] > threshold:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    return img

#處理有雜訊的數字圖片
def image2(img):
    data = img.getdata()
    w, h = img.size
    count = 0
    for x in range(1, h - 1):
        for y in range(1, h - 1):
            #找出每個像素方向
            mid_pixel = data[w * y + x]
            if mid_pixel == 0:
                top_pixel = data[w * (y - 1) + x]
                left_pixel = data[w * y + (x - 1)]
                down_pixel = data[w * (y + 1) + x]
                right_pixel = data[w * y + (x + 1)]
                if top_pixel == 0:
                    count += 1
                if left_pixel == 0:
                    count += 1
                if down_pixel == 0:
                    count += 1
                if right_pixel == 0:
                    count += 1
                if count > 4:
                    img.putpixel((x, y), 0)

    return img


if __name__ == "__main__":

    #字母數字驗證圖
    #main()

    #白底黑字車牌辨識
    captcha = Image.open('C:\MyProject\python\webspider\webspider\imgtemp\car.jpg') # 黑白圖片
    # result = pytesseract.image_to_string(captcha)
    # # 去掉識別結果中的特殊字符
    # exclude_char_list = ' .:\\|\'\"?![],()~@#$%^&*_+-={};<>/¥'
    # text = ''.join([x for x in result if x not in exclude_char_list])
    # print(text)

    captcha = Image.open('C:\MyProject\python\webspider\webspider\imgtemp\images1.jpg')
    # result = convert_img(captcha, 150)  # 像素範圍
    # result = pytesseract.image_to_string(result,lang='chi_tra+eng')
    # # 去掉識別結果中的特殊字符
    # exclude_char_list = ' .:\\|\'\"?![],()~@#$%^&*_+-={};<>/¥\n'
    # text = ''.join([x for x in result if x not in exclude_char_list])
    # print(text)

    captcha = Image.open('C:\MyProject\python\webspider\webspider\imgtemp\images1.jpg')
    result = image2(captcha)
    result = pytesseract.image_to_string(result, lang='chi_tra+eng')
    # 去掉識別結果中的特殊字符
    exclude_char_list = ' .:\\|\'\"?![],()~@#$%^&*_+-={};<>/¥\n'
    text = ''.join([x for x in result if x not in exclude_char_list])
    print(result)