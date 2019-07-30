#!/usr/bin/env python
# coding=utf-8
# Created by JTProgru
# Date: 2019-07-29
# https://jtprog.ru/

__author__ = 'jtprogru'
__version__ = '0.0.1'
__author_email__ = 'mail@jtprog.ru'

from jira import JIRA
import dotenv as d
from pathlib import Path

env = d.get_variables(str(Path(__file__).parent / '.env'))


# Login to Jira API
def jira_login():
    """
    Login to Jira server
    :return: JIRA object
    """
    jira_server = {'server': env['JIRA_SERVER']}
    return JIRA(options=jira_server, basic_auth=(env['JIRA_USER'], env['JIRA_PASS']))


def create_issue(title: str, body: str, project: str, issuetype: str, priority: str) -> str:
    """
    Creating issue in Jira
    :param title:
    :param body:
    :param project:
    :param issuetype:
    :param priority:
    :return:
    """
    jira = jira_login()
    issue_params = {
        'project': {'key': project},
        'summary': title,
        'description': body,
        'issuetype': {'id': issuetype},
        'priority': {'id': priority}
    }
    return jira.create_issue(fields=issue_params).key


def close_issue(issue, status):
    """
    close_issue()
    :param issue:
    :param status:
    :return: None
    """
    jira = jira_login()
    jira.transition_issue(issue, status)


