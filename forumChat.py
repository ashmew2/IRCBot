'''
Read a file and send messaages to the IRC channel
'''
import sopel.module
import subprocess
import time

CHANNEL_NAME='#kolibrios'
SKIP_NUMBER = 1
FUNCTION_LOCK=False
IRC_LOGS="/home/bob/irc.txt"
FORUMCHAT_MESSAGES="/home/bob/forumchat.txt"
try:
    forumChatMessages = open(FORUMCHAT_MESSAGES)
except IOError:
    tempFile = open(FORUMCHAT_MESSAGES, 'w')
    tempFile.close()
    forumChatMessages = open(FORUMCHAT_MESSAGES)

global start_talking
start_talking = False
global messages_to_skip
messages_to_skip = 95

@sopel.module.interval(5)
def send_forumchat_to_IRC(bot):
    global forumChatMessages
    global FUNCTION_LOCK

    if FUNCTION_LOCK == True:
        return
    else:
        FUNCTION_LOCK = True

    global SKIP_NUMBER
    if SKIP_NUMBER != 5:
        SKIP_NUMBER+=1
        
    elif CHANNEL_NAME in bot.channels:
        stuffToSay = []
        for i in range(0,5):
            new_message = forumChatMessages.readline()
            if new_message == '':
                break
            stuffToSay.append(new_message)

        global start_talking
        global messages_to_skip
        
        for i in stuffToSay:
            if start_talking == True:
                bot.msg(CHANNEL_NAME, i)
            else:
                messages_to_skip-=1;
                if messages_to_skip == 0:
                    start_talking = True;
                    
    FUNCTION_LOCK = False

@sopel.module.rule('.*')
def handle_msg(bot, trigger):
    global IRC_LOGS
    ircLogs = open(IRC_LOGS, 'a')
    ircLogs.write(trigger.nick + ': ' + trigger.group() + '\n')
    ircLogs.close()
