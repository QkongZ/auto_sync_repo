import json
import subprocess
import os

# 从配置文件中读取仓库信息
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# 获取GitHub Token（PAT）
github_token = os.environ['PAT']

for repo_info in config['repositories']:
    source_repo = repo_info['source_repo']
    source_branch = repo_info['source_branch']
    destination_branch = repo_info['destination_branch']

    try:
        # 克隆仓库
        subprocess.run(['git', 'clone', source_repo], check=True)
        print(f"Cloned repository: {source_repo}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone repository: {source_repo}")
        print(f"Error message: {e.output}")
        continue

    try:
        # 切换到源分支
        subprocess.run(['git', 'checkout', source_branch], check=True)
        print(f"Switched to source branch: {source_branch}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to switch to source branch: {source_branch}")
        print(f"Error message: {e.output}")
        continue

    try:
        # 推送分支到目标分支
        subprocess.run(['git', 'config', 'user.name', 'GitHub Actions'], check=True)
        subprocess.run(['git', 'config', 'user.email', 'actions@github.com'], check=True)
        subprocess.run(['git', 'push', f'https://{github_token}@github.com/{source_repo}', f'{source_branch}:{destination_branch}'], check=True)
        print(f"Pushed {source_branch} to {destination_branch}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to push {source_branch} to {destination_branch}")
        print(f"Error message: {e.output}")
        continue
