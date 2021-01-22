#!/usr/bin/env python
import ESL
import logger

class Esl():
 def __init__(self,host,port,password):
  self.name = 'Esl'
  self.host = host
  self.port = port
  self.password = password

 def connected(self):
  conn = ESL.ESLconnection(self.host,self.port,self.password)
  if conn.connected():
   log_event = logger.Logger('connected ESL API!')
   log_event.esl_logged(conn)
   return conn
  else:
   log_event = logger.Logger('Log')
   log_event.log_logged('Error connected ESL API!')
