#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

from gitlab import Gitlab

from config import Config


gl = Gitlab(Config.gitlab_url, Config.gitlab_token)
project = gl.projects.get('tsalzmann/gl-test-project')

# csv reference:
# ticketnr - [0]
# prio - [1]
# subject - [2]
# process - [3]
# title - [4]
# assignee - [5]
# status - [6]
# descr - [7]


def getCompany(str):
    if str.find('ENSO') != -1:
        return 'ENSO'
    else:
        return 'DREWAG'


def rowToIssue(row):
    title = '{ticket} - {title}'.format(ticket=row[0], title=row[4])
    company = getCompany(row[2])
    description = (
        'Prozess: {process}\n\n \
        {descr}\n\nBisheriger Bearbeiter: {assignee}'
        .format(process=row[3], descr=row[7], assignee=row[5])
    )
    prio = 'Prio {0}'.format(row[1])
    status = row[6]

    issue = {
        'title': title,
        'description': description,
        'labels': [
            company,
            prio,
            status,
        ]
    }

    project.issues.create(issue)


def convertCSV():
    # Read in csv
    with open('test_data.csv') as csvFile:
        print('Reading csv file...')
        readCSV = csv.reader(csvFile, delimiter=',')

        for index, row in enumerate(readCSV):
            print('Converting row: {}'.format(index))
            rowToIssue(row)


def main():
    convertCSV()

if __name__ == "__main__":
    main()
