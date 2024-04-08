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
    # 打印完整的配置仓库列表
    print(f"处理的仓库列表: {repo_info['source_repo']}")
    source_repo = repo_info['source_repo']
    source_branch = repo_info['source_branch']
    destination_branch = repo_info['destination_branch']
    excludes = repo_info.get('excludes', [])  # 获取需要排除的文件或文件夹列表，默认为空列表

    try:
        # 克隆仓库并切换到源分支
        repo_dir = source_repo.split('/')[-1].split('.git')[0]
        repo = Repo.clone_from(source_repo, repo_dir)
        os.chdir(repo_dir)  # 切换到仓库目录
        repo.git.checkout(source_branch)
        print(f"已克隆仓库 {source_repo} 并切换到源分支 {source_branch}")
    except Exception as e:
        print(f"克隆仓库 {source_repo} 或切换到源分支 {source_branch} 失败")
        print(f"错误信息: {str(e)}")
        continue

    try:
        # 添加目标仓库为远程仓库
        your_repo_url = f"https://{github_token}@github.com/{your_repo_info['username']}/{your_repo_info['repository']}.git"
        repo.create_remote('destination', your_repo_url)

        # 拉取目标分支的最新代码
        try:
            repo.remotes['destination'].fetch(destination_branch)
            repo.git.checkout(destination_branch)
        except Exception:
            # 如果目标分支不存在，先克隆仓库并切换到源分支
            repo = Repo.clone_from(source_repo, repo_dir)
            os.chdir(repo_dir)
            repo.git.checkout(destination_branch)

        # 拉取远程目标仓库分支
        repo.remotes['origin'].pull(source_branch)

        # 合并源分支的代码，排除指定的文件或文件夹
        merge_message = f"合并 {source_branch} 自 {source_repo} 到 {destination_branch}"
        if excludes:
            excludes_string = ', '.join(excludes)
            merge_message += f"（排除 {excludes_string}）"
        # 使用指定的合并策略：theirs 表示保留远程分支的更改
        repo.git.merge(f"origin/{source_branch}", message=merge_message, strategy='theirs')
        for exclude in excludes:
            if os.path.exists(os.path.join(repo.working_dir, exclude)):
                if os.path.isdir(exclude):
                    print(f"排除目录: {exclude}")
                    repo.git.rm('-r', '--cached', exclude)
                else:
                    print(f"排除文件: {exclude}")
                    repo.git.rm('--cached', exclude)
            else:
                print(f"路径不存在: {exclude}")

        # 提交合并的更改
        repo.index.commit(merge_message)
        print("提交更改:", repo.index.diff('HEAD'))

        # 推送源分支到目标分支
        repo.remotes['destination'].push(destination_branch)
        print(f"已推送 {source_branch} 自 {source_repo} 到 {destination_branch} 到您的仓库")
    except Exception as e:
        print(f"处理仓库 {source_repo} 和分支 {source_branch} 时发生错误")
        print(f"错误信息: {str(e)}")
