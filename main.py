#!/usr/bin/env python3
# coding=utf-8
# Created by JTProgru
# Date: 2019-07-29
# https://jtprog.ru/

__author__ = 'jtprogru'
__version__ = '0.0.2'
__author_email__ = 'mail@jtprog.ru'

from pyzabbix import ZabbixAPI
import sys
from utils import *

# Zabbix API
zapi = ZabbixAPI(env['ZBX_SERVER'])
zapi.session.verify = False
zapi.login(user=env['ZBX_USER'], password=env['ZBX_PASS'])

# Get event object with {EVENT.ID}
amsg = parse_message(sys.argv[1])
event = zapi.event.get(eventids=amsg['event_id'])[0]
logging.debug("[*******************] DEBUG: Event -> %s" % event)
body = create_message(amsg)
logging.debug("[*******************] DEBUG: Body -> %s" % body)
# Check Acknowledge field
logging.debug("[*******************] DEBUG: Ack status -> %s" % event['acknowledged'])
if event['acknowledged'] is '0':
    try:
        issue_key = create_issue(title=amsg['subject'],
                                 body=body,
                                 project=env['JIRA_PROJECT'],
                                 issuetype=env['JIRA_ISSUE_TYPE'],
                                 priority=env['JIRA_ISSUE_PRIORITY'])
        logging.debug("[*******************] DEBUG: Issue created: %s" % issue_key)
        zapi.event.acknowledge(eventids=int(amsg['event_id']),
                               action=6,
                               message=issue_key)
        logging.debug("[*******************] DEBUG: Event Acknowledged: %s " % event['eventid'])
        # Add org name
        add_org(keyid=issue_key, org=jira_organization_map[amsg['client']])
        logging.debug("[*******************] DEBUG: Add org name: {0}".format(jira_organization_map[amsg['client']]))
        # Classification issue
        classification_issue(keyid=issue_key, status=env['JIRA_TRANSITION_CLASSIF'])
        logging.debug("[*******************] DEBUG: "
                      "Classification status: {0} -> {1}".format(issue_key,
                                                                 env['JIRA_TRANSITION_CLASSIF']))
        sys.exit(0)
    except Exception as e:
        logging.debug("[*******************] DEBUG: Exception".format(e))

elif event['acknowledged'] == '1':
    try:
        issue_key = zapi.event.get(eventids=int(amsg['event_id']),
                                   output='extend',
                                   select_acknowledges='extend')[0]
        issue_key = issue_key['acknowledges'][0]['message']
        logging.debug("[*******************] DEBUG: Issue key from event: %s" % issue_key)
        # Add comment before closing
        add_comment(keyid=issue_key, comment=body)
        logging.debug("[*******************] DEBUG: Add comment: %s " % body)
        # Close issue
        close_issue(keyid=issue_key, status=env['JIRA_TRANSITION_CLOSE'])
        logging.debug("[*******************] DEBUG: Close issue: {0} -> {1} ".format(issue_key,
                                                                                     env['JIRA_TRANSITION_CLOSE']))
        sys.exit(0)
    except Exception as e:
        logging.debug("[*******************] DEBUG: Exception".format(e))
