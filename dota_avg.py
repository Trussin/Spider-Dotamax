import requests
from lxml import etree
import xlwt

##########################################
# 爬取各英雄整体胜率
##########################################


hero_list_en=['huskar','shredder','axe','slardar','sand_king','undying','omniknight','spirit_breaker','legion_commander','tiny','tidehunter','life_stealer','doom_bringer','bristleback','skeleton_king','rattletrap','alchemist','magnataur','abaddon','kunkka','wisp','dragon_knight','phoenix','beastmaster','tusk','elder_titan','lycan','night_stalker','earthshaker','treant','abyssal_underlord','earth_spirit','chaos_knight','pudge','centaur','brewmaster','sven','nyx_assassin','viper','riki','antimage','morphling','vengefulspirit','phantom_assassin','luna','clinkz','gyrocopter','monkey_king','ember_spirit','drow_ranger','lone_druid','bounty_hunter','terrorblade','naga_siren','mirana','sniper','phantom_lancer','arc_warden','venomancer','nevermore','troll_warlord','slark','bloodseeker','spectre','faceless_void','medusa','templar_assassin','pangolier','meepo','weaver','ursa','juggernaut','broodmother','razor','shadow_shaman','silencer','disruptor','ancient_apparition','invoker','obsidian_destroyer','lina','warlock','dark_seer','crystal_maiden','zuus','lion','lich','jakiro','rubick','techies','chen','ogre_magi','enigma','leshrac','witch_doctor','shadow_demon','keeper_of_the_light','bane','batrider','queenofpain','skywrath_mage','tinker','dazzle','enchantress','necrolyte','winter_wyvern','visage','death_prophet','storm_spirit','dark_willow','pugna','furion','windrunner','oracle','puck']

hero_list_cn=['哈斯卡','伐木机','斧王','斯拉达','沙王','不朽尸王','全能骑士','裂魂人','军团指挥官','小小','潮汐猎人','噬魂鬼','末日使者','钢背兽','冥魂大帝','发条技师','炼金术士','马格纳斯','亚巴顿','昆卡','艾欧','龙骑士','凤凰','兽王','巨牙海民','上古巨神','狼人','暗夜魔王','撼地者','树精卫士','孽主','大地之灵','混沌骑士','帕吉','半人马战行者','酒仙','斯温','司夜刺客','冥界亚龙','力丸','敌法师','变体精灵','复仇之魂','幻影刺客','露娜','克林克兹','矮人直升机','齐天大圣','灰烬之灵','卓尔游侠','德鲁伊','赏金猎人','恐怖利刃','娜迦海妖','米拉娜','狙击手','幻影长矛手','天穹守望者','剧毒术士','影魔','巨魔战将','斯拉克','嗜血狂魔','幽鬼','虚空假面','美杜莎','圣堂刺客','石鳞剑士','米波','编织者','熊战士','主宰','育母蜘蛛','剃刀','暗影萨满','沉默术士','干扰者','远古冰魄','祈求者','殁境神蚀者','莉娜','术士','黑暗贤者','水晶室女','宙斯','莱恩','巫妖','杰奇洛','拉比克','工程师','陈','食人魔魔法师','谜团','拉席克','巫医','暗影恶魔','光之守卫','祸乱之源','蝙蝠骑士','痛苦女王','天怒法师','修补匠','戴泽','魅惑魔女','瘟疫法师','寒冬飞龙','维萨吉','死亡先知','风暴之灵','邪影芳灵','帕格纳','先知','风行者','神谕者','帕克']

heroes_dict_en=dict(zip(['huskar','shredder','axe','slardar','sand_king','undying','omniknight','spirit_breaker','legion_commander','tiny','tidehunter','life_stealer','doom_bringer','bristleback','skeleton_king','rattletrap','alchemist','magnataur','abaddon','kunkka','wisp','dragon_knight','phoenix','beastmaster','tusk','elder_titan','lycan','night_stalker','earthshaker','treant','abyssal_underlord','earth_spirit','chaos_knight','pudge','centaur','brewmaster','sven','nyx_assassin','viper','riki','antimage','morphling','vengefulspirit','phantom_assassin','luna','clinkz','gyrocopter','monkey_king','ember_spirit','drow_ranger','lone_druid','bounty_hunter','terrorblade','naga_siren','mirana','sniper','phantom_lancer','arc_warden','venomancer','nevermore','troll_warlord','slark','bloodseeker','spectre','faceless_void','medusa','templar_assassin','pangolier','meepo','weaver','ursa','juggernaut','broodmother','razor','shadow_shaman','silencer','disruptor','ancient_apparition','invoker','obsidian_destroyer','lina','warlock','dark_seer','crystal_maiden','zuus','lion','lich','jakiro','rubick','techies','chen','ogre_magi','enigma','leshrac','witch_doctor','shadow_demon','keeper_of_the_light','bane','batrider','queenofpain','skywrath_mage','tinker','dazzle','enchantress','necrolyte','winter_wyvern','visage','death_prophet','storm_spirit','dark_willow','pugna','furion','windrunner','oracle','puck'], ['哈斯卡','伐木机','斧王','斯拉达','沙王','不朽尸王','全能骑士','裂魂人','军团指挥官','小小','潮汐猎人','噬魂鬼','末日使者','钢背兽','冥魂大帝','发条技师','炼金术士','马格纳斯','亚巴顿','昆卡','艾欧','龙骑士','凤凰','兽王','巨牙海民','上古巨神','狼人','暗夜魔王','撼地者','树精卫士','孽主','大地之灵','混沌骑士','帕吉','半人马战行者','酒仙','斯温','司夜刺客','冥界亚龙','力丸','敌法师','变体精灵','复仇之魂','幻影刺客','露娜','克林克兹','矮人直升机','齐天大圣','灰烬之灵','卓尔游侠','德鲁伊','赏金猎人','恐怖利刃','娜迦海妖','米拉娜','狙击手','幻影长矛手','天穹守望者','剧毒术士','影魔','巨魔战将','斯拉克','嗜血狂魔','幽鬼','虚空假面','美杜莎','圣堂刺客','石鳞剑士','米波','编织者','熊战士','主宰','育母蜘蛛','剃刀','暗影萨满','沉默术士','干扰者','远古冰魄','祈求者','殁境神蚀者','莉娜','术士','黑暗贤者','水晶室女','宙斯','莱恩','巫妖','杰奇洛','拉比克','工程师','陈','食人魔魔法师','谜团','拉席克','巫医','暗影恶魔','光之守卫','祸乱之源','蝙蝠骑士','痛苦女王','天怒法师','修补匠','戴泽','魅惑魔女','瘟疫法师','寒冬飞龙','维萨吉','死亡先知','风暴之灵','邪影芳灵','帕格纳','先知','风行者','神谕者','帕克']))

heroes_dict=dict(zip( ['哈斯卡','伐木机','斧王','斯拉达','沙王','不朽尸王','全能骑士','裂魂人','军团指挥官','小小','潮汐猎人','噬魂鬼','末日使者','钢背兽','冥魂大帝','发条技师','炼金术士','马格纳斯','亚巴顿','昆卡','艾欧','龙骑士','凤凰','兽王','巨牙海民','上古巨神','狼人','暗夜魔王','撼地者','树精卫士','孽主','大地之灵','混沌骑士','帕吉','半人马战行者','酒仙','斯温','司夜刺客','冥界亚龙','力丸','敌法师','变体精灵','复仇之魂','幻影刺客','露娜','克林克兹','矮人直升机','齐天大圣','灰烬之灵','卓尔游侠','德鲁伊','赏金猎人','恐怖利刃','娜迦海妖','米拉娜','狙击手','幻影长矛手','天穹守望者','剧毒术士','影魔','巨魔战将','斯拉克','嗜血狂魔','幽鬼','虚空假面','美杜莎','圣堂刺客','石鳞剑士','米波','编织者','熊战士','主宰','育母蜘蛛','剃刀','暗影萨满','沉默术士','干扰者','远古冰魄','祈求者','殁境神蚀者','莉娜','术士','黑暗贤者','水晶室女','宙斯','莱恩','巫妖','杰奇洛','拉比克','工程师','陈','食人魔魔法师','谜团','拉席克','巫医','暗影恶魔','光之守卫','祸乱之源','蝙蝠骑士','痛苦女王','天怒法师','修补匠','戴泽','魅惑魔女','瘟疫法师','寒冬飞龙','维萨吉','死亡先知','风暴之灵','邪影芳灵','帕格纳','先知','风行者','神谕者','帕克'],['huskar','shredder','axe','slardar','sand_king','undying','omniknight','spirit_breaker','legion_commander','tiny','tidehunter','life_stealer','doom_bringer','bristleback','skeleton_king','rattletrap','alchemist','magnataur','abaddon','kunkka','wisp','dragon_knight','phoenix','beastmaster','tusk','elder_titan','lycan','night_stalker','earthshaker','treant','abyssal_underlord','earth_spirit','chaos_knight','pudge','centaur','brewmaster','sven','nyx_assassin','viper','riki','antimage','morphling','vengefulspirit','phantom_assassin','luna','clinkz','gyrocopter','monkey_king','ember_spirit','drow_ranger','lone_druid','bounty_hunter','terrorblade','naga_siren','mirana','sniper','phantom_lancer','arc_warden','venomancer','nevermore','troll_warlord','slark','bloodseeker','spectre','faceless_void','medusa','templar_assassin','pangolier','meepo','weaver','ursa','juggernaut','broodmother','razor','shadow_shaman','silencer','disruptor','ancient_apparition','invoker','obsidian_destroyer','lina','warlock','dark_seer','crystal_maiden','zuus','lion','lich','jakiro','rubick','techies','chen','ogre_magi','enigma','leshrac','witch_doctor','shadow_demon','keeper_of_the_light','bane','batrider','queenofpain','skywrath_mage','tinker','dazzle','enchantress','necrolyte','winter_wyvern','visage','death_prophet','storm_spirit','dark_willow','pugna','furion','windrunner','oracle','puck']))

hero_list=['huskar','shredder','axe','slardar','sand_king','undying','omniknight','spirit_breaker','legion_commander','tiny','tidehunter','life_stealer','doom_bringer','bristleback','skeleton_king','rattletrap','alchemist','magnataur','abaddon','kunkka','wisp','dragon_knight','phoenix','beastmaster','tusk','elder_titan','lycan','night_stalker','earthshaker','treant','abyssal_underlord','earth_spirit','chaos_knight','pudge','centaur','brewmaster','sven','nyx_assassin','viper','riki','antimage','morphling','vengefulspirit','phantom_assassin','luna','clinkz','gyrocopter','monkey_king','ember_spirit','drow_ranger','lone_druid','bounty_hunter','terrorblade','naga_siren','mirana','sniper','phantom_lancer','arc_warden','venomancer','nevermore','troll_warlord','slark','bloodseeker','spectre','faceless_void','medusa','templar_assassin','pangolier','meepo','weaver','ursa','juggernaut','broodmother','razor','shadow_shaman','silencer','disruptor','ancient_apparition','invoker','obsidian_destroyer','lina','warlock','dark_seer','crystal_maiden','zuus','lion','lich','jakiro','rubick','techies','chen','ogre_magi','enigma','leshrac','witch_doctor','shadow_demon','keeper_of_the_light','bane','batrider','queenofpain','skywrath_mage','tinker','dazzle','enchantress','necrolyte','winter_wyvern','visage','death_prophet','storm_spirit','dark_willow','pugna','furion','windrunner','oracle','puck']

head = {}
head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19'

i=0
name_avg=[]
rate_avg=[]

#爬取英雄中文名和胜率

url='http://www.dotamax.com/hero/rate/?server=cn&skill=n&ladder=y&time=month' 
r=requests.get(url, headers=head).text
s=etree.HTML(r)
name_avg.append(s.xpath('/html/body/div[2]/div[3]/div[1]/div[2]/table/tbody/tr/td[1]/span/text()'))
rate_avg.append(s.xpath('/html/body/div[2]/div[3]/div[1]/div[2]/table/tbody/tr/td[2]/div[1]/text()'))
    
url='http://www.dotamax.com/hero/rate/?server=cn&skill=h&ladder=y&time=month' 
r=requests.get(url, headers=head).text
s=etree.HTML(r)
name_avg.append(s.xpath('/html/body/div[2]/div[3]/div[1]/div[2]/table/tbody/tr/td[1]/span/text()'))
rate_avg.append(s.xpath('/html/body/div[2]/div[3]/div[1]/div[2]/table/tbody/tr/td[2]/div[1]/text()'))

url='http://www.dotamax.com/hero/rate/?server=cn&skill=vh&ladder=y&time=month' 
r=requests.get(url, headers=head).text
s=etree.HTML(r)
name_avg.append(s.xpath('/html/body/div[2]/div[3]/div[1]/div[2]/table/tbody/tr/td[1]/span/text()'))
rate_avg.append(s.xpath('/html/body/div[2]/div[3]/div[1]/div[2]/table/tbody/tr/td[2]/div[1]/text()'))

list_n=0 
while list_n < 3:   
    i=0
    j=0
    #把英雄名字变为英文
    for heroname_cn in name_avg[list_n]:
        name_avg[list_n][j]=heroes_dict[heroname_cn]
        j=j+1
    #把英雄的名字和胜率按照标准顺序排序
    hero_n=0
    while hero_n < 115:   
        if name_avg[list_n][i]==hero_list[hero_n]:
            name_avg[list_n][i]=name_avg[list_n][hero_n]
            name_avg[list_n][hero_n]=hero_list[hero_n]
            temp=rate_avg[list_n][i]
            rate_avg[list_n][i]=rate_avg[list_n][hero_n]
            rate_avg[list_n][hero_n]=temp
            hero_n=hero_n+1
            i=hero_n
        else:
            i=i+1 
    print (list_n+1,'/3',len(name_avg[list_n]))
    list_n=list_n+1

workbook = xlwt.Workbook(encoding = 'ascii')
worksheet1 = workbook.add_sheet('avg')
for row in range(1,116):
    worksheet1.write(row, 0, hero_list[row-1])

worksheet1.write(0, 1, 'n')
worksheet1.write(0, 2, 'h')
worksheet1.write(0, 3, 'vh')
for col in range(1,4):
    for row in range(1,116):
        worksheet1.write(row, col, rate_avg[col-1][row-1])
workbook.save('Dota_avg.xls')
