#!/usr/bin/env python3
# coding=utf-8
# Created by JTProgru
# Date: 2019-07-29
# https://jtprog.ru/

__author__ = 'jtprogru'
__version__ = '0.0.1'
__author_email__ = 'mail@jtprog.ru'

from pyzabbix import ZabbixAPI
import sys
from utils import *
import urllib3

import logging

# Disable SSL warning
urllib3.disable_warnings()
# Load environment

# Logging configuration
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d]# '
                           u'%(levelname)s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG,
                    filename=env['LOG_FILE_PATH'])

#  Zabbix API
zapi = ZabbixAPI(env['ZBX_SERVER'])
zapi.session.verify = False
# 1.1 Login to Zabbix
zapi.login(user=env['ZBX_USER'], password=env['ZBX_PASS'])
logging.debug("Connected to Zabbix API Version %s" % zapi.api_version())


try:
    # Get event object with {EVENT.ID}
    event = zapi.event.get(eventids=sys.argv[1])[0]
    # Check Acknowledge field
    if event['acknowledged'] is '0':
        keyid = create_issue(title=sys.argv[2],
                             body=sys.argv[3],
                             project=env['JIRA_PROJECT'],
                             issuetype=env['JIRA_ISSUE_TYPE'],
                             priority=env['JIRA_ISSUE_PRIORITY'])

        zapi.event.acknowledge(eventids=int(event['eventid']), action=6, message=keyid)
    elif event['acknowledged'] is '1':
        issue_key = zapi.event.get(eventids=sys.argv[1], output='extend', select_acknowledges='extend')[0]
        issue_key = issue_key['acknowledges'][0]['message']
        close_issue(issue=issue_key, status=env['JIRA_TRANSITION_CLASSIF'])
        close_issue(issue=issue_key, status=env['JIRA_TRANSITION_CLOSE'])


except Exception as e:
    logging.debug("[*] EXCEPTION: %s" % e)



