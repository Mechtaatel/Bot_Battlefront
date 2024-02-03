import discord
from discord.ui import Button, View
import json
import math


class button4v4View(View):

  def __init__(self, ctx, collection, Author, *args, **kwargs):
    # Передайте игрока в качестве аргумента конструктору
    super().__init__(*args, **kwargs, timeout=6000)
    self.ctx = ctx
    self.collection = collection
    self.Author = Author
    self.view = View()
    self.lose_press = 0
    self.win_press = 0

    self.ReaL = []
    self.j = 0
    self.gen_team1 = 0
    self.gen_team2 = 0

    self.button_win = Button(label='Win', style=discord.ButtonStyle.green)
    self.button_lose = Button(label='Lose', style=discord.ButtonStyle.red)
    self.button_remove = Button(label='remove')
    self.button_repeat = Button(label='Repeat',
                                style=discord.ButtonStyle.green)
    self.button_close = Button(label='Close', style=discord.ButtonStyle.red)

    self.DontAgain = 'Вы уже состоите в команде'
    self.PlzReg = "Вы не зарегестрированы.\nДля регестрации воспользуйтесь коммандой /reg"

    Au = {
        'id': ctx.author.id,
        'n': f"{Author['EA_Name']}",
        'r': Author['Rating_4v4'],
        't': 0
    }
    self.Dictionaries_Team = {
        'au': Au,
        't12': {
            'id': 0,
            'n': "`___`",
            'r': 0,
            't': 0
        },
        't13': {
            'id': 0,
            'n': "`___`",
            'r': 0,
            't': 0
        },
        't14': {
            'id': 0,
            'n': "`___`",
            'r': 0,
            't': 0
        },
        't21': {
            'id': 0,
            'n': "`___`",
            'r': 0,
            't': 1
        },
        't22': {
            'id': 0,
            'n': "`___`",
            'r': 0,
            't': 1
        },
        't23': {
            'id': 0,
            'n': "`___`",
            'r': 0,
            't': 1
        },
        't24': {
            'id': 0,
            'n': "`___`",
            'r': 0,
            't': 1
        }
    }

    for key in self.Dictionaries_Team:
      self.Dictionaries_Team[key]['p'] = '⚫'

    for key, value in self.Dictionaries_Team.items():
      if value['t'] == 0:
        self.gen_team1 += value['r']
      elif value['t'] == 1:
        self.gen_team2 += value['r']

    self.list_team = [ctx.author.id]

  async def repeat(self, button, interaction):
    if interaction.user.id in self.list_team and interaction.user.id not in self.ReaL:
      self.ReaL.append(interaction.user.id)
      self.j -= 1
      current_embed = interaction.message.embeds[0]
      current_embed.set_footer(
          text=f"`Желающих повторить:{abs(self.j-8)} | 8`")
      if self.j == 0:
        current_embed.set_footer(text='')
        self.add_item(self.button_win)
        self.add_item(self.button_lose)
        self.add_item(self.button_remove)
        self.remove_item(self.button_repeat)
        self.remove_item(self.button_close)
        for key, value in self.Dictionaries_Team.items():
          value['p'] = '⚫'
        await interaction.response.edit_message(embed=current_embed, view=self)

      else:
        await interaction.response.edit_message(embed=current_embed, view=self)
    elif interaction.user.id in self.ReaL:
      await interaction.response.send_message("Вы не можете нажать дважды",
                                              ephemeral=True)
    else:
      await interaction.response.send_message("Вы не состоите в команде",
                                              ephemeral=True)

  async def close(self, button, interaction):
    if interaction.user.id in self.list_team:
      await interaction.response.edit_message(view=None)
    else:
      await interaction.response.send_message("Вы не состоите в команде",
                                              ephemeral=True)

  async def EloR(self, interaction):

    Q_a = 10**(self.value['r'] / 400)
    Q_b = 10**(self.oppR / 400)
    E_a = Q_a / (Q_a + Q_b)
    if self.value['r'] <= 2100:
      K_a = 32
    elif self.value['r'] <= 2400:
      K_a = 24
    else:
      K_a = 16
    # Игрок - комманда А победители потому 1 - комманда Б победители потому 0
    R_a = self.value['r'] + K_a * (self.value['WorL'] - E_a)
    if R_a < 100:
      R_a = 100
    R_a = math.ceil(R_a)
    self.collection.update_one({"_id": str(self.value['id'])},
                               {"$set": {
                                   "Rating_2v2": R_a
                               }})
    self.interaction = interaction
    self.j += 1
    if self.j == 8:
      self.remove_item(self.button_win)
      self.remove_item(self.button_lose)
      self.remove_item(self.button_remove)
      self.add_item(self.button_repeat)
      self.add_item(self.button_close)
      
      await interaction.response.edit_message(view=self)

  async def before_elo(self, interaction):
    for key, value in self.Dictionaries_Team.items():
      if value['t'] == 0:
        self.value = value
        self.oppR = self.gen_team2
        await self.EloR(interaction)
      elif value['t'] == 1:
        self.value = value
        self.oppR = self.gen_team1
        await self.EloR(interaction)

  async def apdate_embed_gameplay(self, interaction):
    dt = self.Dictionaries_Team
    team1press = 0
    team2press = 0
    team2wl = 2
    team1wl = 2
    # team#wl это команда Победа и проигрыш. 2 это ни то ни другое

    current_embed = interaction.message.embeds[0]
    current_embed.set_field_at(
        1,
        name=
        f"`{dt['au']['r'] + dt['t12']['r'] + dt['t13']['r'] + dt['t14']['r']}`",
        value=f"""
{dt['au']['p']}`{dt['au']['n']}`
{dt['t12']['p']}`{dt['t12']['n']}`
{dt['t13']['p']}`{dt['t13']['n']}`
{dt['t14']['p']}`{dt['t14']['n']}`""",
        inline=True)
    current_embed.set_field_at(
        2,
        name=
        f"`{dt['t21']['r'] + dt['t22']['r'] + dt['t23']['r'] + dt['t24']['r']}`",
        value=f"""
{dt['t21']['p']}`{dt['t21']['n']}`
{dt['t22']['p']}`{dt['t22']['n']}`
{dt['t23']['p']}`{dt['t23']['n']}`
{dt['t24']['p']}`{dt['t24']['n']}`""",
        inline=True)

    current_embed.set_footer(text='')

    for key, value in dt.items():
      if value['t'] == 0 and value['p'] == '🟢':
        team1press += 1
        if team1press == 4:
          team1wl = 1

      elif value['t'] == 1 and value['p'] == '🟢':
        team2press += 1
        if team2press == 4:
          team2wl = 1
      elif value['t'] == 0 and value['p'] == '🔴':
        team1press += 1
        if team1press == 4:
          team1wl = 0
      elif value['t'] == 1 and value['p'] == '🔴':
        team2press += 1
        if team2press == 4:
          team2wl = 0

    if team1wl == 1 and team2wl == 0:
      for key, value in dt.items():
        if value['t'] == 1:
          dt[key]['WorL'] = 1
        elif value['t'] == 0:
          dt[key]['WorL'] = 0
      await self.EloR(interaction)
    elif team1wl == 0 and team2wl == 1:
      for key, value in dt.items():
        if value['t'] == 1:
          dt[key]['WorL'] = 0
        elif value['t'] == 0:
          dt[key]['WorL'] = 1
      await self.EloR(interaction)
    else:
      await interaction.response.edit_message(embed=current_embed, view=self)

  async def win(self, button, interaction):
    totach = "Вы уже нажали на кнопку"
    # Проверяем что бы нажимали именно участники.

    if interaction.user.id in self.list_team:
      if interaction.user.id == self.Dictionaries_Team['au']['id']:
        if self.Dictionaries_Team['au']['p'] == '⚫':
          self.Dictionaries_Team['au']['p'] = '🟢'

          await self.apdate_embed_gameplay(interaction)
        else:
          await interaction.response.send_message(totach, ephemeral=True)

      elif interaction.user.id == self.Dictionaries_Team['t12']['id']:
        if self.Dictionaries_Team['t12']['p'] == '⚫':
          self.Dictionaries_Team['t12']['p'] = '🟢'
          await self.apdate_embed_gameplay(interaction)
        else:
          await interaction.response.apdate_embed_gameplay(totach,
                                                           ephemeral=True)

      elif interaction.user.id == self.Dictionaries_Team['t13']['id']:
        if self.Dictionaries_Team['t13']['p'] == '⚫':
          self.Dictionaries_Team['t13']['p'] = '🟢'
          await self.apdate_embed_gameplay(interaction)
        else:
          await interaction.response.send_message(totach, ephemeral=True)

      elif interaction.user.id == self.Dictionaries_Team['t14']['id']:
        if self.Dictionaries_Team['t14']['p'] == '⚫':
          self.Dictionaries_Team['t14']['p'] = '🟢'
          await self.apdate_embed_gameplay(interaction)
        else:
          await interaction.response.send_message(totach, ephemeral=True)

      elif interaction.user.id == self.Dictionaries_Team['t21']['id']:
        if self.Dictionaries_Team['t21']['p'] == '⚫':
          self.Dictionaries_Team['t21']['p'] = '🟢'
          await self.apdate_embed_gameplay(interaction)
        else:
          await interaction.response.send_message(totach, ephemeral=True)

      elif interaction.user.id == self.Dictionaries_Team['t22']['id']:
        if self.Dictionaries_Team['t22']['p'] == '⚫':
          self.Dictionaries_Team['t22']['p'] = '🟢'
          await self.apdate_embed_gameplay(interaction)
        else:
          await interaction.response.send_message(totach, ephemeral=True)

      elif interaction.user.id == self.Dictionaries_Team['t23']['id']:
        if self.Dictionaries_Team['t23']['p'] == '⚫':
          self.Dictionaries_Team['t23']['p'] = '🟢'
          await self.apdate_embed_gameplay(interaction)
        else:
          await interaction.response.send_message(totach, ephemeral=True)
      elif interaction.user.id == self.Dictionaries_Team['t12']['id']:
        if self.Dictionaries_Team['t24']['p'] == '⚫':
          self.Dictionaries_Team['t24']['p'] = '🟢'
          await self.apdate_embed_gameplay(interaction)
        else:
          await interaction.response.send_message(totach, ephemeral=True)
    else:
      await interaction.response.send_message('Вы не состоите в команде',
                                              ephemeral=True)

  async def lose(self, button, interaction):
    totach = "Вы уже нажали на кнопку"
    if interaction.user.id in self.list_team:
      if interaction.user.id == self.Dictionaries_Team['au']['id']:
        if self.Dictionaries_Team['au']['p'] == '⚫':
          self.Dictionaries_Team['au']['p'] = '🔴'

          await self.apdate_embed_gameplay(interaction)
        else:
          await interaction.response.send_message(totach, ephemeral=True)

      elif interaction.user.id == self.Dictionaries_Team['t12']['id']:
        if self.Dictionaries_Team['t12']['p'] == '⚫':
          self.Dictionaries_Team['t12']['p'] = '🔴'
          await self.apdate_embed_gameplay(interaction)
        else:
          await interaction.response.send_message(totach, ephemeral=True)

      elif interaction.user.id == self.Dictionaries_Team['t13']['id']:
        if self.Dictionaries_Team['t13']['p'] == '⚫':
          self.Dictionaries_Team['t13']['p'] = '🔴'
          await self.apdate_embed_gameplay(interaction)
        else:
          await interaction.response.send_message(totach, ephemeral=True)

      elif interaction.user.id == self.Dictionaries_Team['t14']['id']:
        if self.Dictionaries_Team['t14']['p'] == '⚫':
          self.Dictionaries_Team['t14']['p'] = '🔴'
          await self.apdate_embed_gameplay(interaction)
        else:
          await interaction.response.send_message(totach, ephemeral=True)

      elif interaction.user.id == self.Dictionaries_Team['t21']['id']:
        if self.Dictionaries_Team['t21']['p'] == '⚫':
          self.Dictionaries_Team['t21']['p'] = '🔴'
          await self.apdate_embed_gameplay(interaction)
        else:
          await interaction.response.send_message(totach, ephemeral=True)

      elif interaction.user.id == self.Dictionaries_Team['t22']['id']:
        if self.Dictionaries_Team['t22']['p'] == '⚫':
          self.Dictionaries_Team['t22']['p'] = '🔴'
          await self.apdate_embed_gameplay(interaction)
        else:
          await interaction.response.send_message(totach, ephemeral=True)

      elif interaction.user.id == self.Dictionaries_Team['t23']['id']:
        if self.Dictionaries_Team['t23']['p'] == '⚫':
          self.Dictionaries_Team['t23']['p'] = '🔴'
          await self.apdate_embed_gameplay(interaction)
        else:
          await interaction.response.send_message(totach, ephemeral=True)
      elif interaction.user.id == self.Dictionaries_Team['t12']['id']:
        if self.Dictionaries_Team['t24']['p'] == '⚫':
          self.Dictionaries_Team['t24']['p'] = '🔴'
          await self.apdate_embed_gameplay(interaction)
        else:
          await interaction.response.send_message(totach, ephemeral=True)
    else:
      await interaction.response.send_message('Вы не состоите в команде',
                                              ephemeral=True)

  async def remove(self, button, interaction):
    if interaction.user.id in self.list_team:
      if interaction.user.id == self.Dictionaries_Team['au']['id']:
        self.Dictionaries_Team['au']['p'] = '⚫'
        await self.apdate_embed_gameplay(interaction)
      elif interaction.user.id == self.Dictionaries_Team['t12']['id']:
        self.Dictionaries_Team['t12']['p'] = '⚫'
        await self.apdate_embed_gameplay(interaction)
      elif interaction.user.id == self.Dictionaries_Team['t13']['id']:
        self.Dictionaries_Team['t13']['p'] = '⚫'
        await self.apdate_embed_gameplay(interaction)
      elif interaction.user.id == self.Dictionaries_Team['t14']['id']:
        self.Dictionaries_Team['t14']['p'] = '⚫'
        await self.apdate_embed_gameplay(interaction)
      elif interaction.user.id == self.Dictionaries_Team['t21']['id']:
        self.Dictionaries_Team['t21']['p'] = '⚫'
        await self.apdate_embed_gameplay(interaction)
      elif interaction.user.id == self.Dictionaries_Team['t22']['id']:
        self.Dictionaries_Team['t22']['p'] = '⚫'
        await self.apdate_embed_gameplay(interaction)
      elif interaction.user.id == self.Dictionaries_Team['t23']['id']:
        self.Dictionaries_Team['t23']['p'] = '⚫'
        await self.apdate_embed_gameplay(interaction)
      elif interaction.user.id == self.Dictionaries_Team['t24']['id']:
        self.Dictionaries_Team['t24']['p'] = '⚫'
        await self.apdate_embed_gameplay(interaction)
    else:
      await interaction.response.send_message('Вы не состоите в команде',
                                              ephemeral=True)

  async def apdate_embed(self, interaction):

    dt = self.Dictionaries_Team
    # Функция для обновления сообщения с информацией о команде
    current_embed = interaction.message.embeds[0]

    current_embed.set_field_at(
        1,
        name=
        f"`{dt['au']['r'] + dt['t12']['r'] + dt['t13']['r'] + dt['t14']['r']}`",
        value=
        f"`{dt['au']['n']}`\n`{dt['t12']['n']}`\n`{dt['t13']['n']}`\n`{dt['t14']['n']}`",
        inline=True)

    current_embed.set_field_at(
        2,
        name=
        f"`{dt['t21']['r'] + dt['t22']['r'] + dt['t23']['r'] + dt['t24']['r']}`",
        value=
        f"`{dt['t21']['n']}`\n`{dt['t22']['n']}`\n`{dt['t23']['n']}`\n`{dt['t24']['n']}`",
        inline=True)
    if len(self.list_team) == 8:
      self.remove_item(self.join1)
      self.remove_item(self.join2)
      self.remove_item(self.exit)
      self.add_item(self.button_win)
      self.add_item(self.button_lose)
      self.add_item(self.button_remove)
      await interaction.message.edit(embed=current_embed, view=self)

    else:
      await interaction.response.edit_message(embed=current_embed, view=self)

  async def dictonaries_appdate(self, interaction, check_author, ap):
    self.Dictionaries_Team[ap] = {
        'id': interaction.user.id,
        'n': check_author['EA_Name'],
        'r': check_author['Rating_4v4']
    }
    self.list_team.append(interaction.user.id)
    await self.apdate_embed(interaction)

  @discord.ui.button(label="join",
                     style=discord.ButtonStyle.grey,
                     custom_id="join1")
  async def join1(self, button, interaction):
    check_author = self.collection.find_one({"_id": str(interaction.user.id)})
    # Проверяем. Существует ли человек в нашей базе данных
    if check_author:
      # Человек найден. Проверяем состоит ли он уже в команде или нет.
      if interaction.user.id in self.list_team:
        await interaction.response.send_message(self.DontAgain, ephemeral=True)
      else:
        if self.Dictionaries_Team['t12']['n'] == '`___`':
          ap = 't12'
          await self.dictonaries_appdate(interaction, check_author, ap)
        elif self.Dictionaries_Team['t13']['n'] == '`___`':
          ap = 't13'
          await self.dictonaries_appdate(interaction, check_author, ap)
        elif self.Dictionaries_Team['t14']['n'] == '`___`':
          ap = 't14'
          await self.dictonaries_appdate(interaction, check_author, ap)
    else:
      await interaction.response.send_message(self.PlzReg, ephemeral=True)

  @discord.ui.button(label="join",
                     style=discord.ButtonStyle.blurple,
                     custom_id="join2")
  async def join2(self, button, interaction):

    check_author = self.collection.find_one({"_id": str(interaction.user.id)})
    if check_author:
      if interaction.user.id in self.list_team:
        await interaction.response.send_message(self.DontAgain, ephemeral=True)
      else:
        if self.Dictionaries_Team['t21']['n'] == '`___`':
          ap = 't21'
          await self.dictonaries_appdate(interaction, check_author, ap)
        elif self.Dictionaries_Team['t22']['n'] == '`___`':
          ap = 't22'
          await self.dictonaries_appdate(interaction, check_author, ap)
        elif self.Dictionaries_Team['t23']['n'] == '`___`':
          ap = 't23'
          await self.dictonaries_appdate(interaction, check_author, ap)
          self.list_team.append(interaction.user.id)
        elif self.Dictionaries_Team['t24']['n'] == '`___`':
          ap = 't24'
          await self.dictonaries_appdate(interaction, check_author, ap)

    else:
      await interaction.response.send_message(self.PlzReg, ephemeral=True)

  @discord.ui.button(label="exit",
                     style=discord.ButtonStyle.red,
                     custom_id="exit")
  async def exit(self, button, interaction):
    if interaction.user.id == self.ctx.author.id:
      try:
        await interaction.message.delete()
        await interaction.response.send_message('Вызов удален', ephemeral=True)
      except discord.NotFound:
        await interaction.response.send_message('Вызов уже удален',
                                                ephemeral=True)
      except discord.Forbidden:
        await interaction.response.send_message(
            "У меня нет прав на удаление этого сообщения.", ephemeral=True)
    elif interaction.user.id in self.list_team:
      self.list_team.remove(interaction.user.id)
      for kye, value in self.Dictionaries_Team.items():
        if value['id'] == interaction.user.id:
          self.Dictionaries_Team[kye] = {'id': 0, 'n': "`___`", 'r': 0}
          await self.apdate_embed(interaction)

    else:
      await interaction.response.send_message('Вы не состоите в команде',
                                              ephemeral=True)
