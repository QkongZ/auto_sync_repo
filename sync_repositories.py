import json
import os
import logging
from git import Repo

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def clone_and_switch_branch(repo_info):
    try:
        repo = Repo.clone_from(repo_info['source_repo'], repo_info['source_repo'].split('/')[-1].split('.git')[0])
        repo.git.checkout(repo_info['source_branch'])
        log_info(f"Cloned repository {repo_info['source_repo']} and switched to source branch {repo_info['source_branch']}")
    except Exception as e:
        log_error(f"Failed to clone repository {repo_info['source_repo']} or switch to source branch {repo_info['source_branch']}")
        log_error(f"Error message: {str(e)}")
        return None
    return repo

def merge_and_push(repo, repo_info):
    try:
        merge_message = f"Merged {repo_info['source_branch']} from {repo_info['source_repo']} into {repo_info['destination_branch']}"
        if repo_info['excludes']:
            excludes_string = ', '.join(repo_info['excludes'])
            merge_message += f" (excluding {excludes_string})"
        repo.git.merge(f"origin/{repo_info['source_branch']}", message=merge_message)
        for exclude in repo_info['excludes']:
            if os.path.exists(os.path.join(repo.working_dir, exclude)):
                if os.path.isdir(exclude):
                    log_info(f"Excluding directory: {exclude}")
                    repo.git.rm('-r', '--cached', exclude)
                else:
                    log_info(f"Excluding file: {exclude}")
                    repo.git.rm('--cached', exclude)
            else:
                log_warning(f"Path does not exist: {exclude}")
        repo.index.commit(merge_message)
        repo.git.push('destination', repo_info['destination_branch'])
        log_info(f"Pushed {repo_info['source_branch']} from {repo_info['source_repo']} to {repo_info['destination_branch']} in your repository")
    except Exception as e:
        log_error(f"Error occurred while processing repository {repo_info['source_repo']} and branch {repo_info['source_branch']}")
        log_error(f"Error message: {str(e)}")

# 以下是主程序
logging.basicConfig(filename='sync_log.txt', level=logging.INFO)

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    your_repo_info = config['your_repository']

github_token = os.environ['PAT']

for repo_info in config['repositories']:
    repo = clone_and_switch_branch(repo_info)
    if repo is None:
        continue

    repo.config_writer().set_value("user", "name", "GitHub Actions").release()
    repo.config_writer().set_value("user", "email", "actions@github.com").release()

    your_repo_url = f"https://{github_token}@github.com/{your_repo_info['username']}/{your_repo_info['repository']}.git"
    repo.create_remote('destination', your_repo_url)

    try:
        repo.remotes['destination'].fetch(repo_info['destination_branch'])
        repo.git.checkout(repo_info['destination_branch'])
    except Exception:
        repo.git.checkout('HEAD', b=repo_info['destination_branch'])

    repo.git.pull('destination', repo_info['destination_branch'])

    merge_and_push(repo, repo_info)
