#!/usr/bin/env python

class Configuration:
 def __init__(self):
  self.path = "/etc/zabbix/scripts/test_line"  
  self.host = " "
  self.port = " "
  self.password = " "
  self.caller_name = " "
  self.caller_from_uri = " "
  self.caller_contact_user = " "
  self.auth_username = " "
  self.auth_password = " "
  self.location = "external"
  self.module = "sofia"
  self.called_number = " "
  self.gw = " "
  self.exten = "exten.lua"
  #Trying to call
  self.error_try_sip = "5"
  #Trying to dtmf
  self.error_try_dtmf = "3"
  #Write stage file
  self.stageSip = "sip"
  self.stageRtp = "rtp"
