#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from gitlab import Gitlab

from config import Config


gl = Gitlab(Config.gitlab_url, Config.gitlab_token)
project = gl.projects.get('tsalzmann/gl-test-project')

def issue_to_pm(issue):
    regex = r'^PM-\d+-\d+'
    title = issue.title
    match = re.search(regex, title)
    if match:
        return match.group(0)

    return ''

def get_new_issues(issue, existing_pms):
    if issue['id'] in existing_pms:
        return False
    else:
        return True

def get_company(str):
    if str.find('ENSO') != -1:
        return 'ENSO'
    else:
        return 'DREWAG'

def get_device(str):
    if str.find('Mobile') != -1:
        return 'Mobil'
    else:
        return 'Desktop'

def create_issue(ticket):
    title = '{id} - {subject}'.format(
        id=ticket['id'], subject=ticket['subject'])
    description = ticket['body']
    company = get_company(ticket['subject'])
    device = get_device(ticket['subject'])
    prio = 'Prio {}'.format(ticket['priority'])

    issue = {
        'title': title,
        'description': description,
        'labels': [
            company,
            prio,
            device
        ]
    }

    #  project.issues.create(issue)

def convertJSON():
    existing_issues = project.issues.list(all=True)
    existing_pms = list(map(issue_to_pm, existing_issues))

    with open('tickets.json', 'r') as file:
        data = json.load(file)
        new_issues = list(filter(
            lambda issue: get_new_issues(issue, existing_pms), data))

        print(len(new_issues), len(existing_issues))

        for issue in new_issues:
            print('Creating issue for: {}'.format(issue['id']))
            create_issue(issue)

def main():
    convertJSON()

if __name__ == "__main__":
    main()
