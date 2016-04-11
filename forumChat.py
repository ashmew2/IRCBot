'''
Read a file and send messaages to the IRC channel
'''

import sopel.module
import subprocess
import time

lastmsgs=[]
CHANNEL_NAME='#flood'
SKIP_NUMBER = 1
already_sent_msgs = []
FUNCTION_LOCK=False
IRC_LOGS="/home/bob/irc.txt"

@sopel.module.interval(5)
def send_forumchat_to_IRC(bot):

    global FUNCTION_LOCK
    
    if FUNCTION_LOCK == True:
#        print "Returning from function."
        return
    else:
        FUNCTION_LOCK = True
#        print "Going into Function"

    global already_sent_msgs
    
    global SKIP_NUMBER
    if SKIP_NUMBER != 5:
        SKIP_NUMBER+=1
        
    elif CHANNEL_NAME in bot.channels:
        messages=subprocess.check_output(["tail", "-n", "10", "/home/bob/forumchat.txt"]).split('\n')
        index=len(messages) - 1

        for i in messages:
            if i not in already_sent_msgs:
                bot.msg(CHANNEL_NAME, i)
            
        already_sent_msgs = messages[:]

 #   print "Unlocking Function..."
    FUNCTION_LOCK = False

@sopel.module.rule('.*')
def handle_msg(bot, trigger):
    global IRC_LOGS
    ircLogs = open(IRC_LOGS, 'a')
    ircLogs.write(trigger.nick + ': ' + trigger.group() + '\n')
    ircLogs.close()
