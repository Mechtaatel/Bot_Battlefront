import math

import discord
from discord.ui import View


class button2v2View(View):

  def __init__(self, ctx, collection, Author, *args, **kwargs):
    # Передайте игрока в качестве аргумента конструктору
    super().__init__(*args, **kwargs, timeout=6000)

    self.set = 4


    self.ctx = ctx
    self.collection = collection
    self.Author = Author
    self.view = View()
    self.lose_press = 0
    self.win_press = 0

    self.remove_item(self.lose)
    self.remove_item(self.win)
    self.remove_item(self.close)
    self.remove_item(self.repeat)
    self.remove_item(self.remove)

    self.ReaL = []
    self.j = 0
    self.gen_team1 = 0
    self.gen_team2 = 0

    self.DontAgain = 'Вы уже состоите в команде'
    self.PlzReg = "Вы не зарегестрированы.\nДля регестрации воспользуйтесь коммандой /reg"

    self.Dictionaries_Team = {
        'au': {
            'id': ctx.author.id,
            'n': Author['EA_Name'],
            'r': Author['Rating_2v2'],
            't': 0,
            'p': '⚫'
        },
        't12': {
            'id': 0,
            'n': "`___`",
            'r': 0,
            't': 0,
            'p': '⚫'
        },
        't21': {
            'id': 0,
            'n': "`___`",
            'r': 0,
            't': 1,
            'p': '⚫'
        },
        't22': {
            'id': 0,
            'n': "`___`",
            'r': 0,
            't': 1,
            'p': '⚫'
        }
    }



    self.list_team = [ctx.author.id]
  @discord.ui.button(label="repeat",
   style=discord.ButtonStyle.grey,
   custom_id="repiat")
  async def repeat(self, button, interaction):
    if interaction.user.id in self.list_team and interaction.user.id not in self.ReaL:
      dt = self.Dictionaries_Team
      self.ReaL.append(interaction.user.id)
      self.j -= 1
      current_embed = interaction.message.embeds[0]
      current_embed.set_footer(
          text=f"`Желающих повторить:{abs(self.j-self.set)} | {self.set}`")
      if self.j == 0:
        current_embed.set_field_at(
          1,
          name=
          f"`{dt['au']['r'] + dt['t12']['r']}`",
          value=f"""
{dt['au']['p']}`{dt['au']['n']}`
{dt['t12']['p']}`{dt['t12']['n']}``""",
          inline=True)
        current_embed.set_field_at(
          2,
          name=
          f"`{dt['t21']['r'] + dt['t22']['r']}`",
          value=f"""
{dt['t21']['p']}`{dt['t21']['n']}`
{dt['t22']['p']}`{dt['t22']['n']}`""",
          inline=True)
        current_embed.set_footer(text='')
        self.add_item(self.win)
        self.add_item(self.lose)
        self.add_item(self.remove)
        self.remove_item(self.repeat)
        self.remove_item(self.close)
        self.ReaL.clear()
        for _key, value in self.Dictionaries_Team.items():
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
  @discord.ui.button(label="close",
   style=discord.ButtonStyle.red,
   custom_id="close")
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
    if self.j == self.set:
      self.remove_item(self.win)
      self.remove_item(self.lose)
      self.remove_item(self.remove)
      self.add_item(self.repeat)
      self.add_item(self.close)

      await interaction.response.edit_message(embed=self.C_E, view=self)


  async def before_elo(self, interaction):
    for _key, value in self.Dictionaries_Team.items():
      if value['t'] == 0:
        self.gen_team1 += value['r']
      elif value['t'] == 1:
        self.gen_team2 += value['r']
    for _key, value in self.Dictionaries_Team.items():
      if value['t'] == 0:
        self.value = value
        self.oppR = self.gen_team2 / (self.set / 2)
        print(f'Team 2 {self.oppR}')
        await self.EloR(interaction)
      elif value['t'] == 1:
        self.value = value
        self.oppR = self.gen_team1/ (self.set / 2)
        print(f'Team 1 {self.oppR}')
        await self.EloR(interaction)

  async def apdate_embed_gameplay(self, interaction):
    dt = self.Dictionaries_Team
    team1press = 0
    team2press = 0
    team2wl = 2
    team1wl = 2
    # team#wl это команда Победа и проигрыш. 2 это ни то ни другое

    current_embed = interaction.message.embeds[0]
    current_embed.set_field_at(1,
        name=f"`{dt['au']['r'] + dt['t12']['r']}`",
        value=f"""
{dt['au']['p']}`{dt['au']['n']}`
{dt['t12']['p']}`{dt['t12']['n']}`""",
        inline=True)
    current_embed.set_field_at(2,
        name=f"`{dt['t21']['r'] + dt['t22']['r']}`",
        value=f"""
{dt['t21']['p']}`{dt['t21']['n']}`
{dt['t22']['p']}`{dt['t22']['n']}`""",
        inline=True)

    current_embed.set_footer(text='')
    self.C_E = current_embed

    for _key, value in dt.items():
      if value['t'] == 0 and value['p'] == '🟢':
        team1press += 1
        if team1press == self.set / 2:
          team1wl = 1

      elif value['t'] == 1 and value['p'] == '🟢':
        team2press += 1
        if team2press == self.set / 2:
          team2wl = 1
      elif value['t'] == 0 and value['p'] == '🔴':
        team1press += 1
        if team1press == self.set / 2:
          team1wl = 0
      elif value['t'] == 1 and value['p'] == '🔴':
        team2press += 1
        if team2press == self.set / 2:
          team2wl = 0

    if team1wl == 1 and team2wl == 0:
      for key, value in dt.items():
        if value['t'] == 1:
          dt[key]['WorL'] = 1
        elif value['t'] == 0:
          dt[key]['WorL'] = 0
      await self.before_elo(interaction)
    elif team1wl == 0 and team2wl == 1:
      for key, value in dt.items():
        if value['t'] == 1:
          dt[key]['WorL'] = 0
        elif value['t'] == 0:
          dt[key]['WorL'] = 1
      await self.before_elo(interaction)
    else:
      await interaction.response.edit_message(embed=current_embed, view=self)
  @discord.ui.button(label="win", style=discord.ButtonStyle.green)
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
          await interaction.response.send_message(totach,ephemeral=True)


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

      
    else:
      await interaction.response.send_message('Вы не состоите в команде',
                                              ephemeral=True)

  @discord.ui.button(label="lose",style=discord.ButtonStyle.red)
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
    else:
      await interaction.response.send_message('Вы не состоите в команде',
                                              ephemeral=True)
  @discord.ui.button(label="remove",
   style=discord.ButtonStyle.grey,
   custom_id="remove")
  async def remove(self, button, interaction):
    if interaction.user.id in self.list_team:
      if interaction.user.id == self.Dictionaries_Team['au']['id']:
        self.Dictionaries_Team['au']['p'] = '⚫'
        await self.apdate_embed_gameplay(interaction)
      elif interaction.user.id == self.Dictionaries_Team['t12']['id']:
        self.Dictionaries_Team['t12']['p'] = '⚫'
        await self.apdate_embed_gameplay(interaction)

      elif interaction.user.id == self.Dictionaries_Team['t21']['id']:
        self.Dictionaries_Team['t21']['p'] = '⚫'
        await self.apdate_embed_gameplay(interaction)
      elif interaction.user.id == self.Dictionaries_Team['t22']['id']:
        self.Dictionaries_Team['t22']['p'] = '⚫'
        await self.apdate_embed_gameplay(interaction)
      
    else:
      await interaction.response.send_message('Вы не состоите в команде',
                                              ephemeral=True)

  async def apdate_embed(self, interaction):

    dt = self.Dictionaries_Team
    # Функция для обновления сообщения с информацией о команде
    current_embed = interaction.message.embeds[0]

    current_embed.set_field_at(1,
        name=f"`{dt['au']['r'] + dt['t12']['r']}`",
        value=f"`{dt['au']['n']}`\n`{dt['t12']['n']}``",
        inline=True)

    current_embed.set_field_at(2,
        name=f"`{dt['t21']['r'] + dt['t22']['r']}`",
        value=f"`{dt['t21']['n']}`\n`{dt['t22']['n']}`",
        inline=True)
    if len(self.list_team) == self.set:
      self.remove_item(self.join1)
      self.remove_item(self.join2)
      self.remove_item(self.exit)
      self.add_item(self.win)
      self.add_item(self.lose)
      self.add_item(self.remove)
      await interaction.message.edit(embed=current_embed, view=self)

    else:
      await interaction.response.edit_message(embed=current_embed, view=self)

  async def dictonaries_appdate(self, interaction, check_author, ap, t):
    self.Dictionaries_Team[ap] = {
        'id': interaction.user.id,
        'n': check_author['EA_Name'],
        'r': check_author['Rating_2v2'],
        't': t,
        'p': '⚫'
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
          t = 0
          await self.dictonaries_appdate(interaction, check_author, ap, t)
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
          t = 1
          await self.dictonaries_appdate(interaction, check_author, ap, t)
        elif self.Dictionaries_Team['t22']['n'] == '`___`':
          ap = 't22'
          t = 1
          await self.dictonaries_appdate(interaction, check_author, ap, t)
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

