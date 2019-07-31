#!/usr/bin/env python
# coding=utf-8
# Created by JTProgru
# Date: 2019-07-29
# https://jtprog.ru/

__author__ = 'jtprogru'
__version__ = '0.0.1'
__author_email__ = 'mail@jtprog.ru'

from jira import JIRA
from config import *
import json


# Login to Jira API
def jira_login():
    """
    jira_login()
    :return: JIRA object
    """
    jira_server = {'server': env['JIRA_SERVER']}
    return JIRA(options=jira_server, basic_auth=(env['JIRA_USER'], env['JIRA_PASS']))


# Create issue
def create_issue(title, body, project, issuetype, priority) -> str:
    """
    create_issue()
    :param title:
    :param body:
    :param project:
    :param issuetype:
    :param priority:
    :return: KeyID -> str
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


# Close issue
def close_issue(issue, status):
    """
    close_issue()
    :param issue:
    :param status:
    :return: None
    """
    jira = jira_login()
    jira.transition_issue(issue, status)


# Parse message from {ALERT.MESSAGE}
def parse_message(msg):
    """
    Load JSON data from Zabbix {ALERT.MESSAGE}
    :param msg: JSON as string
    :return: JSON obj
    """
    res = json.loads(str(msg))
    return res


# Create message for Jira
def create_message(pre_msg):
    """
    Create pre-format message for body in Jira issue
    :param pre_msg: JSON-object
    :return: string
    """
    msg = 'Host: {host_name} \n\
Trigger: {trigger_name} \n\
Trigger status: {trigger_status} \n\
Trigger severity: {trigger_severity} \n\
Trigger URL: {problem_url} \n\
Item values: {item_value} \n\
Original event ID: {event_id} '.format(host_name=pre_msg['host_name'],
                                       trigger_name=pre_msg['trigger_name'],
                                       trigger_status=pre_msg['trigger_status'],
                                       trigger_severity=pre_msg['trigger_severity'],
                                       problem_url=pre_msg['problem_url'],
                                       item_value=pre_msg['item_value'],
                                       event_id=pre_msg['event_id'])
    return msg

