#!/usr/bin/env python
from time import sleep
import sys
sys.path.append('../conf/')
import cfg
import esl
import logger
import autodial

class Core(object):
 def __init__(self):
  self.name = "Core"
  self.sip_flag_good = '1'
  self.sip_flag_bad = '0'
  self.rtp_flag_good = '1'
  self.rtp_flag_bad = '0'

 def get_connect_variable(self):
  obj_variable = cfg.Configuration()
  return obj_variable.host, obj_variable.port, obj_variable.password

 def try_connect(self,host,port,password):
  obj_connect = esl.Esl(host,port,password)
  connect = obj_connect.connected()
  return connect

 def autodial(self,connect):
  obj_autodial = cfg.Configuration()
  obj_autodial = autodial.Autodial(
   obj_autodial.caller_name,
   obj_autodial.caller_from_uri,
   obj_autodial.caller_contact_user,
   obj_autodial.auth_username,
   obj_autodial.auth_password,
   obj_autodial.module,
   obj_autodial.location,
   obj_autodial.called_number,
   obj_autodial.gw,
   obj_autodial.exten,
   obj_autodial.path)
  status,channel_state = obj_autodial.dial(connect)
  hangup_cause,dtmf_digest = obj_autodial.dial_status(connect,
   status,channel_state)
  return hangup_cause,dtmf_digest

 def dial_cause(self,cause):
  obj_hangup = cfg.Configuration()
  obj_hangup = autodial.Autodial(
   obj_hangup.caller_name,
   obj_hangup.caller_from_uri,
   obj_hangup.caller_contact_user,
   obj_hangup.auth_username,
   obj_hangup.auth_password,
   obj_hangup.module,
   obj_hangup.location,
   obj_hangup.called_number,
   obj_hangup.gw,
   obj_hangup.exten,
   obj_hangup.path)
  status = obj_hangup.cause(cause)
  return status
 
 def no_dial(self,connect,dial,dtmf,timeuot):
  try_call = cfg.Configuration()
  call_try = Core(); call = 0
  while call != int(try_call.error_try_sip):
   code = call_try.dial_cause(dial)+' - '+'No Answer!'
   call_try.write_log(connect,code); sleep(timeuot)
   dial,dtmf = call_try.autodial(connect)
   if dial == "['NORMAL_CLEARING']":
    return dial,dtmf
   call = call + 1
   if call == 5: call_try.write_tmp(
    call_try.sip_flag_bad,call_try.rtp_flag_bad)
  if call == int(try_call.error_try_sip):
   return dial,dtmf

 def no_dtmf(self,connect,dial,dtmf,timeuot):
  try_call = cfg.Configuration()
  call_try = Core(); call = 0
  while call != int(try_call.error_try_dtmf):
   code = 'Answer - '+'No DTMF!'
   call_try.write_log(connect,code); sleep(timeuot)
   dial,dtmf = call_try.autodial(connect)
   if dial == "['NORMAL_CLEARING']":
    if dtmf == "['0']":
     return dial,dtmf
    if call == 2: call_try.write_tmp(
     call_try.sip_flag_good,call_try.rtp_flag_bad)
   call = call + 1
  if call == int(try_call.error_try_dtmf):
   return dial,dtmf

 def good_test(self,connect,dial,dtmf):
  if dial == 'Answer':
   if dtmf == "['0']":
    write_res = Core();
    write_res.write_log(connect,'Answer Good, DTMF Good!')
    write_res.write_tmp(
     write_res.sip_flag_good,
     write_res.rtp_flag_good); exit()  

 def bad_dial(self,connect,dial,dtmf):
  if dial != "['NORMAL_CLEARING']":
   try_dial = Core();
   dial,dtmf = try_dial.no_dial(connect,dial,dtmf,5)
   if dial != "['NORMAL_CLEARING']":
    try_dial.write_tmp(try_dial.sip_flag_bad,
    try_dial.rtp_flag_bad); exit()
   return dial,dtmf
  return dial,dtmf

 def bad_dtmf(self,connect,dial,dtmf):
  if dtmf != "['0']":
   try_dtmf = Core();
   dial,dtmf = try_dtmf.no_dtmf(connect,dial,dtmf,5)
   if dial != "['NORMAL_CLEARING']":
    return dial,dtmf
   if dtmf != "['0']":
    try_dtmf.write_tmp(
     try_dtmf.sip_flag_good,
     try_dtmf.rtp_flag_bad); exit()
   return dial,dtmf
  return dial,dtmf

 def write_tmp(self,sip,rtp):
  log_event = logger.Logger(" ")
  log_event.tmp_file("SIP",sip)
  log_event.tmp_file("RTP",rtp)

 def write_log(self,connect,code):
  log_event = logger.Logger(code)
  log_event.esl_logged(connect)
  log_event.log_logged('info',code)

if __name__ == "__main__":
 call_daemon = Core()
 host,port,password = call_daemon.get_connect_variable()
 connect = call_daemon.try_connect(host,port,password)
 if connect:
  print "Connected esl"
  dial,dtmf = call_daemon.autodial(connect)
  print "One step dial: "+dial
  print "One step dtmf: "+dtmf
  # if dial and dtmf
  call_daemon.good_test(connect,dial,dtmf)
  print "One step problem try again!"
  print "See log file"
  # if don't dial
  dial,dtmf = call_daemon.bad_dial(connect,dial,dtmf)
  call_daemon.good_test(connect,dial,dtmf)
  # if dial and don't dtmf
  dial,dtmf = call_daemon.bad_dtmf(connect,dial,dtmf)
  call_daemon.good_test(connect,dial,dtmf)
  dial,dtmf = call_daemon.bad_dial(connect,dial,dtmf)
  call_daemon.good_test(connect,dial,dtmf)
 else:
  print "Connected don't established"
  call_daemon.write_tmp(
   call_daemon.sip_flag_bad,
   call_daemon.rtp_flag_bad)
  
