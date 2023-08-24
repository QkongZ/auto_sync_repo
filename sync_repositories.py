import json
import os
from git import Repo

# 从配置文件中读取仓库信息
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    your_repo_info = config['your_repository']

# 获取GitHub Token（PAT）
github_token = os.environ['PAT']

for repo_info in config['repositories']:
    source_repo = repo_info['source_repo']
    source_branch = repo_info['source_branch']
    destination_branch = repo_info['destination_branch']

    repo_name = source_repo.split('/')[-1].split('.git')[0]  # 提取仓库名

    try:
        # 克隆仓库并切换到源分支
        repo = Repo.clone_from(source_repo, repo_name)
        repo.git.checkout(source_branch)
        print(f"Cloned repository {source_repo} and switched to source branch {source_branch}")
    except Exception as e:
        print(f"Failed to clone repository {source_repo} or switch to source branch {source_branch}")
        print(f"Error message: {str(e)}")
        continue

    try:
        # 设置 Git 配置
        repo.config_writer().set_value("user", "name", "GitHub Actions").release()
        repo.config_writer().set_value("user", "email", "actions@github.com").release()

        # 添加目标仓库为远程仓库
        your_repo_url = f"https://{github_token}@github.com/{your_repo_info['username']}/{your_repo_info['repository']}.git"
        repo.create_remote('destination', your_repo_url)

        # 推送源分支到目标分支
        repo.git.push('destination', f'{source_branch}:{destination_branch}')
        print(f"Pushed {source_branch} from {source_repo} to {destination_branch} in your repository")
    except Exception as e:
        print(f"Failed to push {source_branch} from {source_repo} to {destination_branch} in your repository")
        print(f"Error message: {str(e)}")
        continue
