import json
import discord
from discord.ui import View, Select



class role_commands(View):
  def __init__(self, ctx, check_author, guild, role):
    self.check_author = check_author
    self.guild = guild
    self.ctx = ctx
    self.role = role
    
    
  def levelR(self, r, l):
    if r > 1200:
      r -= 400
      l += 1
      return levelR(r, l)
    else:
      return l
  

  def sll(self):
    sl = [
        self.check_author['Rating_1v1'], self.check_author['Rating_2v2'],
        self.check_author['Rating_4v4']
    ]
  
    for i in range(2):
      for j in range(3 - i - 1):
        if sl[j] < sl[j + 1]:
          sl[j], sl[j + 1] = sl[j + 1], sl[j]
    return sl
    
  
  async def switch(self):
    sl = self.sll()
    level = self.levelR(sl[0], 0)

    with open('Rating_commands/Role.json') as f:
      Roles = json.load(f)
    member = self.ctx.user
    roles = member.roles
    role1 = roles[len(roles) - 1]
    
    
    if self.role == 'Dark':
      roleid = 1071606225189470339
    elif self.role == 'Mando':
      roleid = 1073721742406713426
    elif self.role == 'Clone':
      select = Select(options=[ 
      discord.SelectOption(label='104-й Батальон',
        description="Боевое подразделение под командованием Пло Куна.",
        emoji='<:104:1222084458895642717>'),
      discord.SelectOption(label='181-я Танковая дивизия',
        description=''),
      discord.SelectOption(label='212-й Штурмовой батальон',
        description=''),
      discord.SelectOption(label='327-й Звездный корпус',
        description=''),
      discord.SelectOption(label='41-й Элитный корпус',
        description=''),
      discord.SelectOption(label='501-й Легион',
        description=''),
      discord.SelectOption(label='87-й Корпус часовых',
        description=''),
      discord.SelectOption(label='91-й Разведкорпус',
        description='',
        emoji='<:91:1222093887598891078>'),
      discord.SelectOption(label='332-я Рота', 
        description='',
        emoji='<:332:1222097287614959657>'),
      discord.SelectOption(label='Корусантский гвардеец', 
        description='',
        emoji='<:CoruscantGuard:1222097255524335656>')
      ])
      view = View()
      view.add_item(select)
      await self.ctx.interaction.response.send_message('Выберите отряд',view=view)
      async def select_callback(interaction):
        await member.remove_roles(role1)
        await member.add_roles(self.guild.get_role(1221779302606180392))
        await member.add_roles(self.guild.get_role(Roles['C'][select.values[0]]))
        await interaction.response.send_message('Ваша роль обновлена')
        await interaction.message.delete()
      select.callback = select_callback
      return
    else:
      await self.ctx.interaction.response.send_message('Error')
      return

    
    
    for i in Roles.keys():
    
      if roleid in Roles[i] and role1.id in Roles[i]:
        await self.ctx.interaction.response.send_message('Вам не требуется смена роли')
        return
      elif roleid in Roles[i] and role1.id not in Roles[i]:
        if i == 'D':
          await member.remove_roles(role1)
          await member.add_roles(self.guild.get_role(Roles[i][level]))
          await self.ctx.interaction.response.send_message("Ваша роль обнавлена")
          return
        elif i == 'M':
          await member.remove_roles(role1)
          await member.add_roles(self.guild.get_role(Roles[i][0]))
          await self.ctx.interaction.response.send_message("Ваша роль обнавлена")
          return
    