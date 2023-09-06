import json
import os
import logging
from git import Repo

def setup_logging():
    logging.basicConfig(filename='sync_log.txt', level=logging.INFO)

def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

def clone_and_switch(repo_info):
    try:
        repo = Repo.clone_from(repo_info['source_repo'], repo_info['source_repo'].split('/')[-1].split('.git')[0])
        repo.git.checkout(repo_info['source_branch'])
        logging.info(f"Cloned repository {repo_info['source_repo']} and switched to source branch {repo_info['source_branch']}")
        return repo
    except Exception as e:
        logging.error(f"Failed to clone repository {repo_info['source_repo']} or switch to source branch {repo_info['source_branch']}")
        logging.error(f"Error message: {str(e)}")
        return None

def setup_git_config(repo):
    repo.config_writer().set_value("user", "name", "GitHub Actions").release()
    repo.config_writer().set_value("user", "email", "actions@github.com").release()

def add_remote(repo, your_repo_info, github_token):
    your_repo_url = f"https://{github_token}@github.com/{your_repo_info['username']}/{your_repo_info['repository']}.git"
    repo.create_remote('destination', your_repo_url)

def fetch_and_checkout(repo, destination_branch):
    try:
        repo.remotes['destination'].fetch(destination_branch)
        repo.git.checkout(destination_branch)
    except Exception:
        repo.git.checkout('HEAD', b=destination_branch)

def pull(repo, destination_branch):
    repo.git.pull('destination', destination_branch)

def merge_and_exclude(repo, repo_info):
    merge_message = f"Merged {repo_info['source_branch']} from {repo_info['source_repo']} into {repo_info['destination_branch']}"
    if repo_info['excludes']:
        excludes_string = ', '.join(repo_info['excludes'])
        merge_message += f" (excluding {excludes_string})"
    repo.git.merge(f"origin/{repo_info['source_branch']}", message=merge_message)
    for exclude in repo_info['excludes']:
        if os.path.exists(os.path.join(repo.working_dir, exclude)):
            if os.path.isdir(exclude):
                logging.info(f"Excluding directory: {exclude}")
                repo.git.rm('-r', '--cached', exclude)
            else:
                logging.info(f"Excluding file: {exclude}")
                repo.git.rm('--cached', exclude)
        else:
            logging.warning(f"Path does not exist: {exclude}")
    repo.index.commit(merge_message)

def reset_and_merge(repo, repo_info):
    try:
        # 重置目标分支到源分支的状态
        repo.git.reset('--hard', f"origin/{repo_info['source_branch']}")
        # 合并源分支的代码
        merge_message = f"Merged {repo_info['source_branch']} from {repo_info['source_repo']} into {repo_info['destination_branch']}"
        if repo_info['excludes']:
            excludes_string = ', '.join(repo_info['excludes'])
            merge_message += f" (excluding {excludes_string})"
        repo.git.merge(f"origin/{repo_info['source_branch']}", message=merge_message)
    except Exception as e:
        logging.error(f"Failed to reset and merge source branch {repo_info['source_branch']} into destination branch {repo_info['destination_branch']}")
        logging.error(f"Error message: {str(e)}")
        return False
    return True

def push(repo, repo_info):
    repo.git.push('destination', repo_info['destination_branch'])
    logging.info(f"Pushed {repo_info['source_branch']} from {repo_info['source_repo']} to {repo_info['destination_branch']} in your repository")

def main():
    setup_logging()
    config = load_config()
    your_repo_info = config['your_repository']
    github_token = os.environ['PAT']

    for repo_info in config['repositories']:
        repo = clone_and_switch(repo_info)
        if repo is None:
            continue
        setup_git_config(repo)
        add_remote(repo, your_repo_info, github_token)
        fetch_and_checkout(repo, repo_info['destination_branch'])
        pull(repo, repo_info['destination_branch'])
        if not reset_and_merge(repo, repo_info):
            continue
        merge_and_exclude(repo, repo_info)
        push(repo, repo_info)

if __name__ == "__main__":
    main()
