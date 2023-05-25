import requests
import os
import datetime
from github import Github

# 获取当前日期
today = datetime.date.today().strftime('%Y%m%d')

# 请求 Bing 每日壁纸
url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
response = requests.get(url)
data = response.json()

# 获取图片地址
image_url = 'https://www.bing.com' + data['images'][0]['url']

# 存储路径到markdown文件
g = Github(os.environ['GITHUB_TOKEN'])
repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])
path = 'data.md'
content = repo.get_contents(path).decoded_content.decode('utf-8')
lines = content.strip().split('\n')
last_line = lines[-1]
last_value = int(last_line.split('|')[1].strip())
new_value = last_value + 1
new_line = f'| {datetime.now().isoformat()} | {new_value} |\n'
new_content = content + new_line
repo.update_file(path, 'Update data', new_content, repo.get_contents(path).sha)
