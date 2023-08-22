
import json
import subprocess

# 从配置文件中读取仓库信息
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

for repo_info in config['repositories']:
    source_repo = repo_info['source_repo']
    source_branch = repo_info['source_branch']
    destination_branch = repo_info['destination_branch']
    
    # 使用 subprocess 或其他方式执行仓库同步操作
    subprocess.run(['git', 'clone', source_repo])
    subprocess.run(['git', 'checkout', source_branch])
    subprocess.run(['git', 'push', 'origin', f'{source_branch}:{destination_branch}'])
