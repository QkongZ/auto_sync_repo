import json  
import subprocess  
  
# 从配置文件中读取仓库信息  
with open('config.json', 'r') as config_file:  
    config = json.load(config_file)  
  
for repo_info in config['repositories']:  
    source_repo = repo_info['source_repo']  
    source_branch = repo_info['source_branch']  
    destination_branch = repo_info['destination_branch']  
      
    try:  
        # 克隆仓库  
        subprocess.run(['git', 'clone', source_repo])  
        print(f"Cloned repository: {source_repo}")  
    except subprocess.CalledProcessError as e:  
        print(f"Failed to clone repository: {source_repo}")  
        print(f"Error message: {e.output}")  
        continue  
      
    try:  
        # 切换到源分支  
        subprocess.run(['git', 'checkout', source_branch])  
        print(f"Switched to source branch: {source_branch}")  
    except subprocess.CalledProcessError as e:  
        print(f"Failed to switch to source branch: {source_branch}")  
        print(f"Error message: {e.output}")  
        continue  
      
    try:  
        # 推送分支到目标分支  
        subprocess.run(['git', 'push', 'origin', f'{source_branch}:{destination_branch}'])  
        print(f"Pushed {source_branch} to {destination_branch}")  
    except subprocess.CalledProcessError as e:  
        print(f"Failed to push {source_branch} to {destination_branch}")  
        print(f"Error message: {e.output}")  
        continue
