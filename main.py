#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gitlab import Gitlab


gl = Gitlab('http://gitlab.4so.local', 'QsXb2TMz245MhrAxtiRW')


# list all the projects
def list_projects():
    projects = gl.projects.list()
    for project in projects:
        print(project)


def main():
    list_projects()
    print('Hello World')


if __name__ == "__main__":
    main()
