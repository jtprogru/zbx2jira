#!/usr/bin/env python
# coding=utf-8
# Created by JTProgru
# Date: 2019-07-29
# https://jtprog.ru/


from jira import JIRA
from config import *
import json


# Login to Jira API
def jira_login():
    """
    Login to Jira
    :return: JIRA object
    """
    jira_server = {'server': env['JIRA_SERVER']}
    return JIRA(options=jira_server, basic_auth=(env['JIRA_USER'], env['JIRA_PASS']))


# Create issue
def create_issue(title, body, project, issuetype, priority):
    """
    Create issue
    :param title: Summary of issue
    :param body: Description of issue
    :param project: Project key -> ex: JIR
    :param issuetype: Issue type -> ex: Task
    :param priority: Issue priority -> ex: Critical, High, Low
    :return: KeyID -> ex: JIR-1234
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


# Add comment to issue
def add_comment(keyid, comment):
    """
    Add internal comment to issue
    :param keyid: KeyID
    :param comment: Text comment
    :return:
    """
    jira = jira_login()
    jira.add_comment(issue=keyid, body=comment, is_internal=True)


# Classification issue
def classification_issue(keyid, status):
    """
    close_issue()
    :param keyid: KeyID
    :param status: Transition for closing issue
    :return: None
    """
    jira = jira_login()
    jira.transition_issue(keyid, status)


# Add organization name
def add_org(keyid, org):
    """
    Add client name in custom field
    :param keyid: KeyID
    :param org: Array with client ID -> ex: [4]
    :return:
    """
    jira = jira_login()
    issue = jira.issue(id=keyid)
    issue.update(fields={"customfield_11200": org})


# Close issue
def close_issue(keyid, status):
    """
    close_issue()
    :param keyid: KeyID
    :param status: Transition for closing issue
    :return: None
    """
    jira = jira_login()
    jira.transition_issue(keyid, status)


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
