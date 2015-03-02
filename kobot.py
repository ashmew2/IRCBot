#Todo: 

from willie.module import commands
import willie.module

users=[]
helpmsg = 'Welcome to #KolibriOS. Ask KolibriOS|Yogev for more help! (Or use !cmd)'
learn_cmdlist = {}
fixed_cmdlist = ['sethelp', 'learn', ,'help', 'logs', 'cmd', 'info', 'wiki']

@commands('sethelp')
def sethelp(bot, trigger):
    if not trigger.group(2):
        return

    if trigger.admin:
        global helpmsg
        bot.reply('Setting helpmsg to : ' + trigger.group(2))
        helpmsg = trigger.group(2);
    else:
        bot.reply('You do not have privileges for this command.')
        
@commands('learn')
def learn(bot, trigger):
    usage_str = 'Usage : !learn !newcommand NEW COMMAND TEXT'
    
    if not trigger.group(2):
        bot.reply(usage_str)
        return
            
    if not trigger.admin:
        bot.reply('You aren\'t allowed to teach me!')
        return
    else:
        words = trigger.group(2).split(' ')
        finalword = ''
        
        if len(words) < 2:
            bot.reply(usage_str)
            return
        else: #Enough commands were supplied
            if words[0][0] != '!':
                finalword = '!' + words[0]
            else:
                finalword = words[0]

            cmdstring = ''
            for i in range(1, len(words)):
                cmdstring+=str(words[i])
                cmdstring+=' '

            learn_cmdlist[finalword] = cmdstring

            bot.reply('Added: ' + finalword + ' = ' + cmdstring)
            
@commands('help')
def help(bot, trigger):
    bot.reply(helpmsg)

@commands('logs')
def logs(bot, trigger):    
    bot.reply('Check out (temporary) logs at http://pastebin.com/18S9gwpX')

@commands('cmd')
def cmd(bot, trigger):
    bot.reply('Supported commands : !info !logs !wiki !help !cmd !sethelp')

@commands('info')
def info(bot, trigger):
    bot.reply('Visit the KolibriOS board at board.kolibrios.org')
    
@commands('wiki')
def wiki(bot, trigger):
    bot.reply('Visit KolibriOS wiki at http://wiki.kolibrios.org/')

#trigger.group contains the entire thing.
@willie.module.rule('.*')
def print_help(bot, trigger):
    if trigger.nick not in users:
        users.append(trigger.nick)

        if learn_cmdlist.has_key(trigger.group()):
            bot.reply(learn_cmdlist[trigger.group()]
        elif trigger.group() not in fixed_cmdlist:  #Change to any command in command list
            bot.reply(helpmsg)
                      
    elif learn_cmdlist.has_key(trigger.group()):
        bot.reply(learn_cmdlist[trigger.group()]
        
#GSoC related stuff comes later. Below this part.
@commands('addtask')
def addtask(bot, trigger):
    if trigger.admin:
        bot.say('As you wish.')
    else:
        bot.say('You dont have permissions sadly.')

#kolibri_user is the default username for IRCC on Kolibri. So we need to reuse them :)        
@willie.module.rule('.*')
@willie.module.event("PART", "QUIT")
def handle_part(bot, trigger):
    if(trigger.nick[:12] == 'kolibri_user'):        
        users.remove(trigger.nick)
#        bot.say(trigger.nick + 'has left the channel. Reusing this nick.')
#    else:
#        bot.say(trigger.nick + 'has left the channel. NOT Reusing.')
