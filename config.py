# coding=utf-8
# Created by JTProgru
# Date: 2019-07-29
# https://jtprog.ru/

import urllib3
import dotenv
from pathlib import Path
import logging

# Disable SSL warning
urllib3.disable_warnings()
# Load environment
env = dotenv.get_variables(str(Path(__file__).parent / '.env'))
# Logging configuretion
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d]# '
                           u'%(levelname)s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG,
                    filename=env['LOG_FILE_PATH'])

zbx_severity_map = {
    '0': 'Not classified',
    '1': 'Information',
    '2': 'Warning',
    '3': 'Average',
    '4': 'High',
    '5': 'Disaster',
}

zbx_action_ack_map = {
    'close': 1,  # - Close problem
    'ack': 2,  # - Acknowledge problem
    'msg': 4,  # - Add message 'message=' is deprecated
    'chsvrty': 8  # - Change severity for
}

jira_organization_map = {
    "client1":
        [1],
    "client2":
        [2],
    "client3":
        [3],
}
