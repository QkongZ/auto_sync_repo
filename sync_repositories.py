import json  
import subprocess  
  
# 从配置文件中读取仓库信息  
with open('config.json', 'r') as config_file:  
    config = json.load(config_file)  
    repositories = config['repositories']  
    source_branch = config['source_branch']  
    destination_branch = config['destination_branch']  
  
# 执行仓库同步操作  
for repo in repositories:  
    repo_url = repo['source_repo']  
    print(f"Cloning repository: {repo_url}")  
    subprocess.run(['git', 'clone', repo_url])  
    print(f"Switched to source branch: {source_branch}")  
    subprocess.run(['git', 'checkout', source_branch])  
    print(f"Pushing {source_branch} to {destination_branch}")  
    subprocess.run(['git', 'push', 'origin', f'{source_branch}:{destination_branch}'])  
    print("--------------------------------------------------------")
