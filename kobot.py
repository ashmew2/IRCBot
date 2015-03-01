#Todo: 

from willie.module import commands
import willie.module

users=[]
helpmsg = 'Welcome to #KolibriOS. Ask KolibriOS|Yogev for more help! (Or use !cmd)'

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

@commands('help')
def help(bot, trigger):
    bot.say(helpmsg)

@commands('logs')
def logs(bot, trigger):    
    bot.say('Check out (temporary) logs at http://pastebin.com/18S9gwpX')

@commands('cmd')
def cmd(bot, trigger):
    bot.say('Supported commands : !info !logs !wiki !help !cmd !sethelp')

@commands('info')
def info(bot, trigger):
    bot.say('Visit the KolibriOS board at board.kolibrios.org')
    
@commands('wiki')
def wiki(bot, trigger):
    bot.say('Visit KolibriOS wiki at http://wiki.kolibrios.org/')

@willie.module.rule('.*')
def print_help(bot, trigger):
    if trigger.nick not in users:
          bot.reply(helpmsg)
          users.append(trigger.nick)    
    
#GSoC related stuff comes later. Below this part.
@commands('addtask')
def addtask(bot, trigger):
    if trigger.admin:
        bot.say('As you wish.')
    else:
        bot.say('You dont have permissions sadly.')        
        
