path = "./sound/"
log_level = "NOTICE"
date = os.date("%d:%m:%Y-%H:%M:%S");
loop = 2
number_dtmf = " "

function call_test(path,loop,log_level,number_dtmf)
 freeswitch.consoleLog(log_level, date.." :CALL-BOT dialplan start ! - \n")
 session:answer()
 while (loop > 0) do
  if (session:ready() == true) then
   session:setAutoHangup(false)
   session:sleep(5000)
   session:streamFile(path.."hello.wav")
   freeswitch.consoleLog(log_level, date.." :CALL-BOT send dtmf - "..number_dtmf.." - \n")
   session:execute("playback","silence_stream://1000")
   session:execute("send_dtmf","#")
   session:sleep(5000)
   session:execute("send_dtmf",number_dtmf)
   session:sleep(5000)
   digits = session:getDigits(1,"",9000);
   if (digits == "0")  then
    freeswitch.consoleLog(log_level, date.." :CALL-BOT recv dtmf - "..digits.." - \n")
    session:streamFile(path.."goodbye.wav")
   end
  else
   return
  end;
 loop = loop - 1
 end
 freeswitch.consoleLog(log_level, date.." :CALL-BOT hangup ! \n")
 session:hangup()
end;

call_test(path,loop,log_level,number_dtmf)
