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
# 获取 GitHub API 认证信息
g = Github(os.environ['GITHUB_TOKEN'])
# 获取代码仓库
repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])
# 读取 data.md 文件内容
path = 'data.md'
content = repo.get_contents(path).decoded_content.decode('utf-8')
# 修改文件内容
new_content = content.replace('old_value', 'new_value')
# 提交文件修改
repo.update_file(path, 'Update data', new_content, repo.get_contents(path).sha)
