import discord
from discord.ui import Button, View
import pymongo
import json
import math



class RepeatOrCloseV1(discord.ui.View):
  def __init__(self,ctx,player,db):
    super().__init__(timeout=600)
    
    self.ctx = ctx
    self.player = player
    self.repeat_press1 = False
    self.repeat_press2 = False
    self.i = 0
    self.j = 0
    self.db = db
    
    

  @discord.ui.button(label="Reapet", style=discord.ButtonStyle.green)
  async def repeat(self,button,interaction):
    if interaction.user.id == int(self.player):
      
      self.repeat_press1 = True
      if self.repeat_press2:
        self.remove_item(self.close)
        button.disabled = True
        view1 = ratingV1Button(self.ctx, self.player, self.db)
        await interaction.response.edit_message(
          content=f"""<@{self.ctx.author.id}> Игрок <@{self.player}> принял вызов!""",
          view=view1  
        )
        
    if interaction.user.id == int(self.ctx.author.id):
      
      self.repeat_press2 = True
      if self.repeat_press1:
        self.remove_item(self.close)
        button.disabled = True
        view1 = ratingV1Button(self.ctx, self.player,self.db)
        await interaction.response.edit_message(
          content=f"""<@{self.ctx.author.id}> Игрок <@{self.player}> принял вызов!""",
          view=view1
        )

  @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
  async def close(self,button,interaction):
    event = [int(self.player), self.ctx.author.id]
    for i in event:
      if i == interaction.user.id:
        await interaction.response.edit_message(view=None)

  async def on_timeout(self):
    for ithem in self.children:
      if isinstance(ithem, discord.ui.Button):
        ithem.disabled = True
      await self.ctx.edit_message(view=self)
        
    
      
    
  

class ratingV1Button(discord.ui.View):
  def __init__(self,ctx,player,db):
    super().__init__(timeout=600)
    self.ctx = ctx
    self.player = player
    self.loseU = None
    self.winU = None
    self.lose_press = False
    self.win_press = False
    self.i = 0
    self.j = 0
    self.event = [self.ctx.author.id, self.player]
    self.db = db

  @discord.ui.button(label='Win', style=discord.ButtonStyle.green)
  async def win(self, button, interaction):
    # Проверяем что бы нажимали именно участники.
    for i in self.event:
      if str(i) == str(interaction.user.id):
        if self.loseU != str(interaction.user.id):
          # Сохраняем все в self что бы один игрок не мог нажать на все кнопки
          winUser = str(interaction.user.id)
          self.winU = winUser 
          button.disabled = True
          # Запоминаем нажатие кнопки
          self.win_press = True
          # Если вторая кнопка уже была нажата то то запускаем цикл расчета рейтинга
          await interaction.response.edit_message(view=self)
          if self.lose_press:
            await self.perform_both_button_pressed_action(interaction)
            
        else:
          # Сообщение для хитрого игрока что все таки решил нажать на кнопку
          await interaction.response.send_message(
            'Вы не можете нажать за своего оппонента', ephemeral=True)

  @discord.ui.button(label='Lose', style=discord.ButtonStyle.red)
  async def lose(self, button, interaction):

    for i in self.event:
      if str(i) == str(interaction.user.id):
        if self.winU != str(interaction.user.id):
          # Делаем все тоже самое и для второй кнопки
          loseUser = str(interaction.user.id)
          self.loseU = loseUser
          self.lose_press = True
          button.disabled = True
          await interaction.response.edit_message(view=self)
          
          if self.win_press:
            await self.perform_both_button_pressed_action(interaction)
          
        else:
          await interaction.response.send_message(
            'Вы не можете нажать за своего оппонента', ephemeral=True)

  async def perform_both_button_pressed_action(self,interaction):
    # with open('Rating_commands/rating_ds.json','r') as f:
    #   Rating_ds = json.load(f)
    collection = self.db['Collection_data']

    winU_db = collection.find_one({"_id": self.winU})
    loseU_db = collection.find_one({"_id":self.loseU})

    # Win = Rating_ds[self.winU]
    # Lose = Rating_ds[self.loseU]
    A = winU_db['Rating_1v1']
    B = loseU_db['Rating_1v1']

    Q_a = 10 ** (A / 400)
    Q_b = 10 ** (B / 400)
    E_a = Q_a / (Q_a + Q_b)
    E_b = Q_b / (Q_a + Q_b)

    if A <= 2100:
        K_a = 32
    elif A <= 2400:
        K_a = 24
    else:
        K_a = 16

    if B <= 2100:
        K_b = 32
    elif B <= 2400:
        K_b = 24
    else:
        K_b = 16

    S_a = 1
    S_b = 0

    if S_a + S_b == 1:
        R_a = A + K_a * (S_a - E_a)
        R_b = B + K_b * (S_b - E_b)
    else:
        print('skatina, ti vvel ne pravilno')
    if R_a < 100:
        R_a = 100
    if R_b < 100:
        R_b = 100
    R_a = math.ceil(R_a)
    R_b = math.ceil(R_b)
    

    collection.update_one({"_id": self.winU}, {"$set": {"Rating_1v1": R_a}})
    collection.update_one({"_id": self.loseU}, {"$set": {"Rating_1v1": R_b}})
    # Win['Rating_1v1'] = R_a
    # Lose['Rating_1v1'] = R_b
    # with open('Rating_commands/rating_ds.json','w') as f:
    #     json.dump(Rating_ds, f)

    try:
      # Try to edit the original message if response already sent
      view2 = RepeatOrCloseV1(self.ctx, self.player, self.db)
      await interaction.edit_original_response(content=
                                              f"""
                                                Победитель: <@{self.winU}> (`{R_a}`) | Пороигравший: <@{self.loseU}> (`{R_b}`)""",
                                                view=view2
                                                )
    except discord.errors.InteractionResponded:
      print('Error')
    


  @discord.ui.button(label='Complaint')
  async def complaint(self, button, interaction):
    uId = interaction.user.id
    if uId == int(self.player):
      self.i += 1
      if self.i == 1:
        await interaction.response.send_message(
          """Вы не согласны со мнением вашего соперника? 
          Нажмите еще раз что бы подтвердить действие""",
          ephemeral=True)
      else:
        self.i += 1
        await interaction.response.edit_message(
        content=f"""Игрок <@{interaction.user.id}> решил что <@{self.ctx.author.id}>
        нажал не туда/играл не честно""",
          view=None) 

    elif uId == int(self.ctx.author.id):
      self.j += 1
      if self.j == 1:
        await interaction.response.send_message(
          """Вы не согласны со мнением вашего соперника?\n
          Нажмите еще раз что бы подтвердить действие""",
          ephemeral=True)
      else:
        self.i += 1
        await interaction.response.edit_message(
        content=f"""Игрок <@{interaction.user.id}> решил что <@{self.player}>
        нажал не туда/играл не честно""",
          view=None) 

    else:
      await interaction.response.send_message(
        'Это предназначено не для вас', ephemeral=True)

  async def on_timeout(self):
    for ithem in self.children:
      if isinstance(ithem, discord.ui.Button):
        ithem.disabled = True
      await self.ctx.edit_message(view=self)
  




class button1v1View(View):

  def __init__(self, ctx, player,db, *args, **kwargs):
    # Передайте игрока в качестве аргумента конструктору
    super().__init__(*args, **kwargs, timeout=600)
    # *aeds **kwargs:
    #  *args и **kwargs являются соглашениями в Python для работы с переменным
    #  количеством аргументов в функциях:
    #
    # *args - используется для передачи неопределенного количества аргументов функции.
    #   Он позволяет функции принимать любое количество позиционных аргументов в виде
    #   кортежа (tuple).
    #
    # **kwargs - используется для передачи неопределенного количества именованных
    #   аргументов функции. Это позволяет функции принимать аргументы в виде
    #   словаря (dictionary), где ключи являются именами аргументов, а
    #   значения — соответствующими данными.
    #
    # В контексте класса button1v1View, использование *args и **kwargs позволяет
    # создатель класса передавать дополнительные позиционные и именованные аргументы в
    # конструктор super(), который их будет использовать или передавать в
    # класс-родитель,от которого идет наследование, если это необходимо.

    self.ctx = ctx
    self.player = str(player) # Сохраняем игрока в переменную self.player вместо player
    self.db = db

  @discord.ui.button(label='Go',
                     style=discord.ButtonStyle.green,
                     custom_id='Soglas')
  async def go(self, button, interaction):
    if interaction.user.id == int(self.player):


      # Удаляем кнопку Нет
      self.remove_item(self.no)
      # Отключаем кнопку Go
      button.disabled = True

       # Добавляем кнопки
      view1 = ratingV1Button(self.ctx, self.player, self.db)
      await interaction.response.edit_message(
        content=f"""<@{self.ctx.author.id}> Игрок <@{self.player}> принял вызов!""",
        view=view1
      )
      # Подтверждаем и сохраняем все в self


    else:
      await interaction.response.send_message(
          'Ты не можешь отвечать на этот вызов', ephemeral=True)

  @discord.ui.button(label='No',
                     style=discord.ButtonStyle.danger,
                     custom_id='otkaz')
  async def no(self, button, interaction):
    if interaction.user.id == int(self.player):
      # Отключаем все кнопки если игрок отказывается.
      button1 = [x for x in self.children if x.custom_id == 'Soglas'][0]
      button1.disabled = True
      button.disabled = True

      await interaction.response.edit_message(
      content=f'Игрок <@{self.player}> отказался', view=self)
    else:
      await interaction.response.send_message(
          'Ты не можешь отвечать на этот вызов', ephemeral=True)

  async def on_timeout(self, interaction):
    for ithem in self.children:
      if isinstance(ithem, discord.ui.Button):
        ithem.disabled = True
    await interaction.response.edit_message(
      content=f'Игрок <@{self.player}> не явился на вызов',
                                      ephemeral=True)

  

