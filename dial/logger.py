#!/usr/bin/env python
from datetime import datetime
import cfg

class Logger():
 def __init__(self,alert):
  self.name = 'Logger'
  self.bot = 'CALL-BOT'
  self.level = 'NOTICE'
  self.alert = alert
  self.date = datetime.strftime(datetime.now(),
   '%d:%m:%Y-%H:%M:%S')

 def esl_logged(self,connect):
  data = self.level+' '+self.bot+' '+self.alert
  connect.api('log',data)

 def log_logged(self,level,data):
  obj_log = cfg.Configuration()
  if level == 'info':
   file_path = obj_log.path+'/log/log_info.log'
  if level == 'debug':
   file_path = obj_log.path+'/log/log_debug.log'
  file = open(file_path, 'a')
  data = self.date+' '+data
  file.write(data +"\n")
  file.close()

 def tmp_file(self,stage,data):
  obj_log = cfg.Configuration()
  if stage == "SIP": name_tmp = obj_log.stageSip
  if stage == "RTP": name_tmp = obj_log.stageRtp
  file_path = obj_log.path+'/tmp/'+name_tmp+'.tmp'
  file = open(file_path, 'w')
  file.write(data +"\n")
  file.close()
