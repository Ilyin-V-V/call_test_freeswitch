### <b>This script tests telephone lines using the following algorithm:</b>
    He dials the number for verification and makes extension dialing of the extension number
    waits for a response in the form of a dtmf signal - 0
### <b>Schema works</b>
#### <b>Shoulder A:</b>
    | A pbx (call number,send dtmf) |
    | B pbx (ivr speak,ext_number) |
    | C pbx (send dtmf 0) |
#### <b>Shoulder B:</b>
    | A pbx (get_dtmf 0) |
    | B pbx (relay_dtmf 0) |
    | C pbx (send dtmf 0) |
### <b>Files projects:</b>
    core.py - executable script
    autodial.py - module for calling number B
    cfg.py - config file
    esl.py - esl freeswitsh connector
    logger.py - logging module
    exten.lua - dialplan
    sip.tmp, rtp.tmp - result file
### <b>Install</b>
    Esl must be configured on freeswitch
    a) Install python dependencies - python-ESL, datetime, regex
    b) Create a folder for example /etc/zabbix/scripts/test_line
    c) Copy the files to test_line and set the patch variable in the cfg.conf
    d) If you need monitoring from zabbix
       Create a file /etc/zabbix/zabbix_agentd.d/userparameter_test.conf
        UserParameter = host.line-sip-test, cat /etc/zabbix/scripts/test_line/sip.tmp
        UserParameter = host.line-rtp-test, cat /etc/zabbix/scripts/test_line/rtp.tmp
       Create and configure triggers on zabbix
        name - host.line-rtp-test
        value:
         {host.domain.com:host.line-rtp-test.last()><1
         {host.domain.com:host.line-sip-test.last()><1
    e) Dialplan pbx C might look like this:
       exten => ext_number,1,Answer()
       exten => ext_number,n,Wait(5)
       exten => ext_number,n,SendDTMF(0)
       exten => ext_number,n,HangUp()
### <b>Configure</b>
    a) The cfg.conf file:
       Esl:
        host - ip address pbx
        port - port pbx
        password - password esl
       Sip:
        caller_name - display user agent
        caller_from_uri - caller_from_uri (sip: user@host-operator.domain)
        caller_contact_user - caller_contact_user (gw + user)
        auth_username - user
        auth_password - password
        location - name context pbx
        module - sofia
        called_number - called A
        gw - gw operator (host.domain.com)
        error_try_sip - number of dial iterations
        error_try_dtmf - number of dtmf iterations
        stageSip - sip monitoring file name for zabbix
        stageRtp - the name of the rtp monitoring file for zabbix
    b) The exten.conf file:
       loop - number of dtmf in one dialog
       number_dtmf - extension dialing number
