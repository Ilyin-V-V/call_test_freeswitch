#!/usr/bin/env python
import logger
import cfg
import re

class Autodial():
 def __init__(self,
  caller_name,caller_from_uri,caller_contact_user,auth_username,
  auth_password,module,location,called_number,gw,exten,path):
  self.name = 'Autodial'
  self.caller_name = caller_name
  self.caller_from_uri = caller_from_uri
  self.caller_contact_user = caller_contact_user
  self.auth_username = auth_username
  self.auth_password = auth_password
  self.module = module
  self.location = location
  self.called_number = called_number
  self.gw = gw
  self.exten = exten
  self.path = path

 def dial(self,connect):
  if connect:
   log_event = logger.Logger('Dial originate!'); log_event.esl_logged(connect)
   uuid = connect.api('create_uuid').getBody()
   connect.events('plain','all'); connect.filter('Unique-ID',uuid)
   sip_url = '{origination_caller_id_name='+self.caller_name+'}'+\
                   '{sip_from_uri='+self.caller_from_uri+'}'+\
                   '{sip_contact_user='+self.caller_contact_user+'}'+\
                   '{sip_auth_username='+self.auth_username+'}'+\
                   '{sip_auth_password='+self.auth_password+'}'+\
                   '{origination_uuid='+uuid+'}'+\
                   self.module+"/"+self.location+"/"+self.called_number+\
                   "@"+self.gw+" &lua("+self.path+"extensions/"+self.exten+")"
   status = connect.bgapi('originate',sip_url)
   return status,uuid+' '+'state'
  else:
   log_event = logger.Logger('Log')
   log_event.log_logged('Error dial originate!')

 def dial_event(self,connect,channel_state):
  event = connect.recvEvent()
  if event:
   state = connect.api("uuid_getvar",channel_state).getBody()
   event = (event.serialize("json"))
   hangup_cause = str(re.findall('\"Hangup-Cause\":\s\"(\w+)\"',event))
   hangup_cause = str(re.findall("\['\w+\',\s\'(\w+)\'\]",hangup_cause))
   answer = str(re.findall('\"Event-Name\":\s\"(\w+)\"',event))
   application = str(re.findall('\"Application\":\s\"(\w+)\"',event))
   application_data = str(re.findall('\"Application-Data\":\s\"[^,]+',event))
   event_name = str(re.findall('\"Event-Name\":\s\"(\w+)\"',event))
   dtmf_digest = str(re.findall('\"DTMF-Digit\":\s\"(\w+)\"',event))
   evnt_debug_log = event_name+' - '+event
   log_event = logger.Logger(evnt_debug_log)
   log_event.log_logged('debug',evnt_debug_log)
   return hangup_cause,answer,dtmf_digest

 def dial_status(self,connect,status,channel_state):
  dialog_create = False
  while connect:
     obj_event = Autodial(self.caller_name,self.caller_from_uri,
      self.caller_contact_user,self.auth_username,self.auth_password,
      self.module,self.location,self.called_number,self.gw,self.exten,self.path)
     hangup_cause,answer,dtmf_digest = obj_event.dial_event(connect,channel_state)
     if answer == "['CHANNEL_ANSWER']":
      log_event = logger.Logger("CHANNEL_ANSWER"); log_event.esl_logged(connect)
      dialog_create = True
     elif hangup_cause != "[]":
       return hangup_cause,dtmf_digest
     if dialog_create:
       if dtmf_digest == "['0']":
        return 'Answer',dtmf_digest

 def cause(self,status):
  if status:
   if status == "['CALL_REJECTED']" or\
    status == "['OUTGOING_CALL_BARRED']" or\
    status == "['INCOMING_CALL_BARRED']" or\
    status == "['BEARERCAPABILITY_NOTAUTH']":
    return "403"
   elif status == "['UNALLOCATED_NUMBER']" or\
    status == "['NO_ROUTE_TRANSIT_NET']" or\
    status == "['NO_ROUTE_DESTINATION']":
    return "404"
   elif status == "['NO_USER_RESPONSE']":
    return "408"
   elif status == "['NUMBER_CHANGED']" or\
    status == "['REDIRECTION_TO_NEW_DESTINATION']":
    return "410"
   elif status == "['NO_ANSWER']" or\
    status == "['SUBSCRIBER_ABSENT']" or\
    status == "['NORMAL_UNSPECIFIED']":
    return "480"
   elif status == "['EXCHANGE_ROUTING_ERROR']":
    return "483"
   elif status == "['INVALID_NUMBER_FORMAT']":
    return "484"
   elif status == "['USER_BUSY']":
    return "486"
   elif status == "['ORIGINATOR_CANCEL']":
    return "487"
   elif status == "['BEARERCAPABILITY_NOTIMPL']" or\
    status == "['INCOMPATIBLE_DESTINATION']":
    return "488"
   else:
    return status
