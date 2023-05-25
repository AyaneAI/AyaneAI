import requests
import os
import datetime
from github import Github
import re

# 获取当前日期
today = datetime.date.today().strftime('%Y%m%d')

# 请求 Bing 每日壁纸
url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
response = requests.get(url)
data = response.json()

# 获取图片地址
image_info = data['images'][0]
image_url = 'https://www.bing.com' + image_info['url']
image_title = image_info['title']
image_copyright = image_info['copyright']

# 获取 GitHub API 认证信息
g = Github(os.environ['GITHUB_TOKEN'])
# 获取代码仓库
repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])

# 修改 bing_wallpaper.md
# 读取 bing_wallpaper.md 文件内容
file_path = 'bing_wallpaper.md'

# 获取文件原内容
content = ''
if os.path.exists(file_path):
    content = repo.get_contents(file_path).decoded_content.decode('utf-8')

# 增量插入内容
new_content = f'{today} | [{image_copyright}]({image_url})<br>'
if content:
    new_content = content + new_content

if os.path.exists(file_path):
    repo.update_file(file_path, 'Update data', new_content, repo.get_contents(file_path).sha)
else:
    repo.create_file(file_path, 'Create data', new_content)

# 修改 README.md
# 读取 bing_wallpaper.md 文件内容
file_path = 'README.md'

# 获取文件原内容
content = ''
if os.path.exists(file_path):
    content = repo.get_contents(file_path).decoded_content.decode('utf-8')

# 使用正则表达式匹配注释并提取它们之间的内容
pattern = r"<!-- BING-WALLPAPER:START -->(.*?)<!-- BING-WALLPAPER:END -->"
matches = re.findall(pattern, content, re.DOTALL)

# 替换图片
image_md = "![" + image_copyright + "](" + image_url + "'" + image_title + "')"
for match in matches:
    content = content.replace(match, image_md)

if os.path.exists(file_path):
    repo.update_file(file_path, 'Update data', content, repo.get_contents(file_path).sha)