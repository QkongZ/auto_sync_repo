import json
import os
import logging
from git import Repo

# 设置日志记录
logging.basicConfig(filename='sync_log.txt', level=logging.INFO)

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
    excludes = repo_info.get('excludes', [])  # 获取需要排除的文件或文件夹列表，默认为空列表

    try:
        # 克隆仓库并切换到源分支
        repo = Repo.clone_from(source_repo, source_repo.split('/')[-1].split('.git')[0])
        repo.git.checkout(source_branch)
        logging.info(f"Cloned repository {source_repo} and switched to source branch {source_branch}")
    except Exception as e:
        logging.error(f"Failed to clone repository {source_repo} or switch to source branch {source_branch}")
        logging.error(f"Error message: {str(e)}")
        continue

    try:
        # 设置 Git 配置
        repo.config_writer().set_value("user", "name", "GitHub Actions").release()
        repo.config_writer().set_value("user", "email", "actions@github.com").release()

        # 添加目标仓库为远程仓库
        your_repo_url = f"https://{github_token}@github.com/{your_repo_info['username']}/{your_repo_info['repository']}.git"
        repo.create_remote('destination', your_repo_url)

        # 拉取源分支的最新代码
        repo.git.pull('origin', source_branch)

        # 拉取目标分支的最新代码
        repo.remotes['destination'].fetch(destination_branch)
        repo.git.checkout(destination_branch)
        repo.git.pull('destination', destination_branch)

        # 合并源分支的代码，排除指定的文件或文件夹
        merge_message = f"Merged {source_branch} from {source_repo} into {destination_branch}"
        if excludes:
            excludes_string = ', '.join(excludes)
            merge_message += f" (excluding {excludes_string})"
        repo.git.merge(f"origin/{source_branch}", message=merge_message)
        for exclude in excludes:
            if os.path.exists(os.path.join(repo.working_dir, exclude)):
                if os.path.isdir(exclude):
                    logging.info(f"Excluding directory: {exclude}")
                    repo.git.rm('-r', '--cached', exclude)
                else:
                    logging.info(f"Excluding file: {exclude}")
                    repo.git.rm('--cached', exclude)
            else:
                logging.warning(f"Path does not exist: {exclude}")


        # 提交合并的更改
        repo.index.commit(merge_message)

        # 推送源分支到目标分支
        repo.git.push('destination', destination_branch)
        logging.info(f"Pushed {source_branch} from {source_repo} to {destination_branch} in your repository")
    except Exception as e:
        logging.error(f"Error occurred while processing repository {source_repo} and branch {source_branch}")
        logging.error(f"Error message: {str(e)}")
