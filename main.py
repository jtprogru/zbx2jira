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

#  Zabbix API
zapi = ZabbixAPI(env['ZBX_SERVER'])
zapi.session.verify = False
# 1.1 Login to Zabbix
zapi.login(user=env['ZBX_USER'], password=env['ZBX_PASS'])
# logging.info("Connected to Zabbix API Version %s" % zapi.api_version())


def main():
    try:
        # Get event object with {EVENT.ID}
        amsg = parse_message(sys.argv[1])
        event = zapi.event.get(eventids=amsg['event_id'])[0]
        body = create_message(amsg)
        # Check Acknowledge field
        if event['acknowledged'] is '0':
            keyid = create_issue(title=amsg['subject'],
                                 body=body,
                                 project=env['JIRA_PROJECT'],
                                 issuetype=env['JIRA_ISSUE_TYPE'],
                                 priority=env['JIRA_ISSUE_PRIORITY'])
            zapi.event.acknowledge(eventids=int(amsg['event_id']), action=6, message=keyid)
        elif event['acknowledged'] is '1':
            issue_key = zapi.event.get(eventids=int(amsg['event_id']),
                                       output='extend',
                                       select_acknowledges='extend')[0]
            issue_key = issue_key['acknowledges'][0]['message']
            # Add comment before closing
            add_comment(keyid=issue_key, comment=body)
            # Classification issue
            classification_issue(keyid=issue_key, status=env['JIRA_TRANSITION_CLASSIF'], org=jira_organization_map[amsg['client']])
            # Close issue
            close_issue(keyid=issue_key, status=env['JIRA_TRANSITION_CLOSE'])


    except Exception as e:
        logging.critical("[*] CRITICAL: %s" % e)


if __name__ == '__main__':
    main()
    sys.exit(0)
