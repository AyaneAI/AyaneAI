import requests
import os
import datetime

# 获取当前日期
today = datetime.date.today().strftime('%Y%m%d')

# 请求 Bing 每日壁纸
url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
response = requests.get(url)
data = response.json()

# 获取图片地址
image_url = 'https://www.bing.com' + data['images'][0]['url']

# 下载图片
response = requests.get(image_url)

# 创建文件夹
os.makedirs('images', exist_ok=True)

with open(f'images/{today}.jpg', 'wb') as f:
    f.write(response.content)

print(os.listdir('images'))
