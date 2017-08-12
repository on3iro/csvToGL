import os


class Config:
    gitlab_url = os.environ.get('GITLAB_URL')
    gitlab_token = os.environ.get('GITLAB_TOKEN')
