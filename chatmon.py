# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import subprocess
import time
import re
import getpass
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import threading

password = getpass.getpass()

POLL_INTERVAL=10
MESSAGE_FILE="/home/bob/forumchat.txt"
open(MESSAGE_FILE, 'w').close()

IRC_FILE="/home/bob/irc.txt"

global MY_USERNAME
MY_USERNAME = "IRC"

driver = webdriver.Firefox()
driver.get("http://board.kolibrios.org/chat.php")

elem = driver.find_element_by_name("username")
elem.send_keys(MY_USERNAME)

elem = driver.find_element_by_name("password")
elem.send_keys(password)
elem.send_keys(Keys.RETURN)

# <input class="post" name="username" size="25" value="" tabindex="1" type="text">
i=0

lastuser=''
lastmsg=''

polled_msgs = []
global already_written_msgs
already_written_msgs= []
msgs_to_write = []

global parsed_message
jobparsed_message = ''

global irc_messages
irc_messages = []

global already_sent_irc_messages
already_sent_irc_messages = []

class MyHTMLParser(HTMLParser):

    postlink = False
    postlink_local = False

    def handle_starttag(self, tag, attrs):
        global parsed_message
        if tag == "img":
            local_image = False
            alt_emoticon = ''
            img_src = ''

            for attr in attrs:
                if attr[0] == 'src':
                    img_src = attr[1]

                    if attr[1][0:2] == './':
                        local_image = True

                if attr[0] == 'alt':
                    alt_emoticon = attr[1]

            if local_image == True:
                parsed_message += alt_emoticon
            else:
                parsed_message += img_src
        else:
            self.postlink_local = False
            self.postlink = False
            href_value = ''

            for attr in attrs:
                if attr[0] == 'class':
                    if attr[1] == 'postlink':
                        self.postlink = True
                    elif attr[1] == 'postlink-local':
                        self.postlink_local = True
                if attr[0] == 'href':
                    href_value = attr[1]

            if self.postlink == True or self.postlink_local == True:
                parsed_message += ' ' + href_value

    def handle_endtag(self, tag):
        pass
#        print "End tag  :", tag

    def handle_data(self, data):
        pass
#        print "Data     :", data

        global parsed_message

        data = unicode(data, 'utf-8')
#        edata=data.encode('utf-8','ignore')

        if self.postlink == True or self.postlink_local == True:
            self.postlink = False
            self.postlink_local = False
            return

        if data[0:14] == 'viewtopic.php?':
            parsed_message += 'board.kolibrios.org/'

        parsed_message += data
#        print "Data     :", data

    def handle_comment(self, data):
        pass
#        print "Comment  :", data

    def handle_entityref(self, name):
        global parsed_message
        c = unichr(name2codepoint[name])

        parsed_message += c
#        print "Named ent:", c

    def handle_charref(self, name):
        global parsed_message

        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))

        parsed_message += c

#   print "Num ent  :", c
    def handle_decl(self, data):
        pass
#   print "Decl     :", data

parser = MyHTMLParser()
global ircMessageFile
try:
    ircMessageFile = open(IRC_FILE)
except IOError:
    tempFile = open(IRC_FILE, 'w')
    tempFile.close()
    ircMessageFile = open(IRC_FILE)

while True:
    global parsed_message
    global already_written_msgs
    global ircMessageFile
    global MY_USERNAME

    x = driver.page_source
    time.sleep(POLL_INTERVAL)

###Handle the Forum Chat
###Read the messages from forum Chat
###Add the logs from Forum Chat to MESSAGES FILE.
    driver.refresh();

    x=x.encode('utf-8','ignore')
    msgs=re.findall('postauthor.*', x)
#    print len(msgs)

    polled_msgs = []
    for i in msgs:
        username = i[i.find('addtext') + 12:i.find('[/b]')]

        if username == MY_USERNAME:
            continue

        usermsg  = i[i.find('span class="postbody"') + 22:i.find('</span>')]
        parsed_message = ''
        parser.feed(usermsg)
        usermsg = parsed_message[:]

        #Cut the initial part when someone talks to IRC on ForumChat.
        if usermsg[0:4] == "IRC:":
            usermsg = usermsg[4:]

        #usermsg contains some embedded HTML tags.
        #We should ignore all tags.

        polled_msgs.append((username, usermsg))

    msgs_to_write = []
    for i in polled_msgs:
        if i not in already_written_msgs:
            msgs_to_write.append(i)

    already_written_msgs = polled_msgs[:]

    if len(msgs_to_write) != 0:
        FileHandle = open(MESSAGE_FILE, 'a')

        for i in msgs_to_write[::-1]:
#           print 'Writing ' + str(i)
            FileHandle.write('[' + i[0] + ']: ' + i[1] + '\n')

        FileHandle.close()

    stuffToSay = []
    for i in range(0,5):
        new_message = ircMessageFile.readline()
        if new_message == '':
            break
        stuffToSay.append(new_message)

    message_fc = driver.find_element_by_name("message")
    submit_fc = driver.find_element_by_name("submit")

    for i in stuffToSay:
        if i.strip() == "":
            continue

        i=unicode(i.decode('utf-8'))
#        print 'IRC: ' + i
        message_fc.send_keys(i)
        submit_fc.click()
        time.sleep(2)

###Handling of Forum Chat incoming messages complete.
##-------------------------------------------------------------

###Handle messages which arrived on IRC.
###Read the file and add it.
###Basically, write the message in the chat box. Press Submit.

###End of IRC incoming messages handle.

#This should never be reached. But just for completeness.
driver.close()
