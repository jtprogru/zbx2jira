# zbx2jira 

Интеграция системы мониторинга Zabbix и системы Jira ServiceDesk.

Реализовано на Python 3.7. Проверено на Python 3.6.
Данная реализация имеет специфику и не является универсальной.
Многое зависит от используемого проекта в Jira - тут реализовано под Jira ServiceDesk.
Так же зависит от используемого Workflow в проекте ServiceDesk.  

Функционал, который необходимо реализовать:  
- [x] todo: 1. При переходе триггера в состояние `PROBLEM` отправлять запрос в Jira API на
создание новой заявки в проекте `ServiceDesk`;
- [x] todo: 1.1. Login to Zabbix API; 
- [x] todo: 1.2. Получить `EventID`; 
- [x] todo: 1.3. Проверить событие с `EventID` на состояние `Acknowledge`;
- [x] todo: 1.3.1. Если в поле `Acknowledge` стоит `0` отправлять запрос в Jira, 
далее стандартная процедура регистрации заявки;
- [x] todo: 1.3.2. Если в поле `Acknowledge` стоит `1` получить `KeyID` из поля `Acknowledge`; 
- [ ] todo: 2. При создании заявки в отдельное поле - `customfields` - необходимо вписывать `EventID` из Zabbix. 
Необходимо для построения связи `1 <-> 1` между заявкой и сработавшим триггером в мониторинге;
- [x] todo: 2.1. Login to Jira API;
- [x] todo: 2.2. Create Issue;
- [ ] todo: 2.3. Необходимо отдельное поле `customfield` для вписывания значения 
- [ ] todo: 3. По заполненому полю `customfield` получить `KeyID` из Jira и 
вписать в поле `Acknowledge` триггера в Zabbix;
- [x] todo: 4. При изменении статуса триггера в Zabbix на `OK` - т.е. проблема 
разрешилась - взять `KeyID` из поля `Acknowledge` и отправить запрос в Jira API на закрытие заявки с указанным `KeyID`;


Настройки подгружаются с помощью внутреннего модуля `dotenv` из локального файла `.env`. 
Примерное содержимое файла `.env`:
```bash
ZBX_SERVER = 'https://zabbix.example.com'
ZBX_USER = 'zbxuser'
ZBX_PASS = 'zbxpass'
JIRA_SERVER = 'https://jira.example.com'
JIRA_USER = 'jirauser'
JIRA_PASS = 'jirapass'
JIRA_PROJECT = 'PROJ'  # ServiceDesk Project Key
JIRA_ISSUE_TYPE = '10511'  # Issue type ID: Task/Question 
JIRA_ISSUE_PRIORITY = '12121'  # Issue priority for task
JIRA_TRANSITION_CLASSIF = '11'  # Transition ID 
JIRA_TRANSITION_CLOSE = '21'  # Another transition ID
LOG_FILE_PATH = '/var/log/pyproject/zbxjira.log'  # Path to log file
```

