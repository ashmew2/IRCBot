#Todo: 

from willie.module import commands

@commands('help')
def help(bot, trigger):
    bot.say('Welcome to #KolibriOS. Ask KolibriOS|Yogev for more help! (Or use !cmd)')

@commands('logs')
def logs(bot, trigger):    
    bot.say('Check out (temporary) logs at http://pastebin.com/18S9gwpX')

@commands('cmd')
def cmd(bot, trigger):
    bot.say('Supported commands : !info !logs !wiki !help !cmd')

@commands('info')
def info(bot, trigger):
    bot.say('Visit the KolibriOS board at board.kolibrios.org')
    
@commands('wiki')
def wiki(bot, trigger):
    bot.say('Visit KolibriOS wiki at http://wiki.kolibrios.org/')

    
#GSoC related stuff comes later. Below this part.
@commands('addtask')
def addtask(bot, trigger):
    if trigger.admin:
        bot.say('As you wish.')
    else:
        bot.say('You dont have permissions sadly.')        
        
