import discord
from discord.ui import Button, View
import json
import math



class RepeatOrCloseV2(discord.ui.View):
  def __init__(self,ctx,collection,interaction,
   AuthorID,Team1ID,Team2ID,Team3ID,
   list_team,
   Team1N,
   Team2N,
   Team3N,
   AuthorN,
  ):
    super().__init__(timeout=3600)


    self.ctx = ctx
    self.collection = collection


    self.AuthorID = AuthorID
    self.Team1ID = Team1ID
    self.Team2ID = Team2ID
    self.Team3ID = Team3ID
    self.list_team = list_team
    self.Team2N = Team2N
    self.Team2R = collection.find_one({"_id":f"{Team2ID}"})["Rating_2v2"]
    self.Team3N = Team3N
    self.Team3R = collection.find_one({"_id":f"{Team3ID}"})["Rating_2v2"]

    self.AuthorN = AuthorN
    self.AuthorR = collection.find_one({"_id":f"{AuthorID}"})["Rating_2v2"]
    self.Team1N = Team1N
    self.Team1R = collection.find_one({"_id":f"{Team1ID}"})["Rating_2v2"]
    self.i =0


    self.ReaL = []

  @discord.ui.button(label="Reapet", style=discord.ButtonStyle.green)
  async def repeat(self,button,interaction):
    if interaction.user.id in self.list_team and interaction.user.id not in self.ReaL:
      self.ReaL.append(interaction.user.id)
      self.i +=1
      current_embed = interaction.message.embeds[0]
      current_embed.set_footer(text=f"`Желающих повторить:{self.i} | 4`")
      if self.i == 4:
        current_embed.set_footer(text='') 
        view2 = Rating_2v2(self.ctx, self.collection,interaction,
           self.AuthorID,self.Team1ID, self.Team2ID, self.Team3ID,
           self.list_team,
           self.Team1N,self.Team1R,                       
           self.Team2N,self.Team2R,
           self.Team3N,self.Team3R,
           self.AuthorN,self.AuthorR
          )
        await interaction.response.edit_message(embed=current_embed,view=view2)

      else:
        await interaction.response.edit_message(embed=current_embed,view=self)
    elif interaction.user.id in self.ReaL:
      await interaction.response.send_message("Вы не можете нажать дважды",
                                              ephemeral=True)
    else:
      await interaction.response.send_message("Вы не состоите в команде",ephemeral=True)




  
      
  @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
  async def close(self,button,interaction):
    if interaction.user.id in self.list_team:
      await interaction.response.edit_message(view=None)
    else:
      await interaction.response.send_message("Вы не состоите в команде",ephemeral=True)




class Rating_2v2(View):
  def __init__(self,ctx,collection,interaction,
               AuthorID,Team1ID,Team2ID,Team3ID,
               list_team,
               Team1N, Team1R,
               Team2N, Team2R,
               Team3N, Team3R,
               AuthorN, AuthorR
              ):
    super().__init__(timeout=3600)

    
    self.ctx = ctx
    self.collection = collection

    
    self.AuthorID = AuthorID
    self.Team1ID = Team1ID
    self.Team2ID = Team2ID
    self.Team3ID = Team3ID
    self.list_team = list_team

    
    self.AuP = '⚫'
    self.T2P = '⚫'
    self.T3P = '⚫'
    self.T1P = '⚫'
    
    self.lose_press = 0
    self.win_press = 0
    
    self.Team2N = Team2N
    self.Team2R = Team2R
    self.Team3N = Team3N
    self.Team3R = Team3R
  
    self.AuthorN = AuthorN
    self.AuthorR = AuthorR
    self.Team1N = Team1N
    self.Team1R = Team1R

    self.j=0
    

    

  async def EloR(self,interaction):
    self.j += 1
    Q_a = 10 ** (self.R / 400)
    Q_b = 10 ** (self.oppR / 400)
    E_a = Q_a / (Q_a + Q_b)
    if self.R <= 2100:
      K_a = 32
    elif self.R <= 2400:
      K_a = 24
    else:
      K_a = 16
    # Игрок - комманда А победители потому 1 - комманда Б победители потому 0
    R_a = self.R + K_a * (self.ind - E_a)
    if R_a < 100:
      R_a = 100
    R_a = math.ceil(R_a)
    self.collection.update_one({"_id":self.i},{"$set":{"Rating_2v2":R_a}})
    self.interaction = interaction
    if self.j ==4:
      current_embed = interaction.message.embeds[0]
      current_embed.set_field_at(1,name=f"`{self.AuthorR+self.Team1R}`",
         value=f"{self.AuP}`{self.AuthorN}`\n{self.T1P}`{self.Team1N}`",inline=True)


      current_embed.set_field_at(2, name=f"`{self.Team2R+self.Team3R}`",
         value=f"{self.T2P}`{self.Team2N}`\n{self.T3P}`{self.Team3N}`",inline=True)
      
      view2 = RepeatOrCloseV2(self.ctx, self.collection,interaction,
       self.AuthorID,self.Team1ID, self.Team2ID, self.Team3ID,
       self.list_team,self.Team1N,self.Team2N,self.Team3N,self.AuthorN)
      await interaction.response.edit_message(embed=current_embed,view=view2)
    
    



  async def goRating(self,interaction):
    for i in self.list_team:
      if i == self.AuthorID or i ==self.Team1ID:
        self.i = f"{i}"
        self.ind = self.team1
        if i == self.Team1ID:
          self.R = self.Team1R
        else:
          self.R = self.AuthorR
        self.oppR = (self.Team2R + self.Team3R) / 2
        await self.EloR(interaction)
      elif i == self.Team2ID or i == self.Team3ID:
        self.i = f"{i}"
        self.ind = self.team2
        if i == self.Team2ID:
          self.R = self.Team2R
        else:
          self.R = self.Team3R
        self.oppR = (self.AuthorR + self.Team1R) / 2
        await self.EloR(interaction)
        
      
      
    
   

  async def apdate_embed(self,interaction):
    current_embed = interaction.message.embeds[0]
    current_embed.set_field_at(1,name=f"`{self.AuthorR+self.Team1R}`",
       value=f"{self.AuP}`{self.AuthorN}`\n{self.T1P}`{self.Team1N}`",inline=True)

    
    current_embed.set_field_at(2, name=f"`{self.Team2R+self.Team3R}`",
       value=f"{self.T2P}`{self.Team2N}`\n{self.T3P}`{self.Team3N}`",inline=True)

    current_embed.set_footer(text='') 
    
    if self.AuP == '🟢' and self.T1P == '🟢' and self.T2P == '🔴' and self.T3P == '🔴':
      self.team1 = 1
      self.team2 = 0
      await self.goRating(interaction)
    elif self.AuP == '🔴' and self.T1P == '🔴' and self.T2P =='🟢' and self.T3P =='🟢':
      self.team1 = 0
      self.team2 = 1
      await self.goRating(interaction)
    else:
      await interaction.response.edit_message(embed=current_embed,view=self)
    
      
      

  

  

    
  @discord.ui.button(label='Win', style=discord.ButtonStyle.green)
  async def win(self, button, interaction):
    totach = "Вы уже нажали на кнопку"
    # Проверяем что бы нажимали именно участники.
    if interaction.user.id in self.list_team:
      if interaction.user.id == self.AuthorID:
        if self.AuP == '⚫':
          self.AuP = '🟢'
          
          await self.apdate_embed(interaction)
        else:
          await interaction.response.send_message(totach,ephemeral=True)
       
      elif interaction.user.id == self.Team1ID:
        if self.T1P == '⚫':
          self.T1P = '🟢'
          await self.apdate_embed(interaction)
        else:
          await interaction.response.send_message(totach,ephemeral=True)
        
      elif interaction.user.id == self.Team2ID:
        if self.T2P == '⚫':
          self.T2P = '🟢'
          
          await self.apdate_embed(interaction)
        else:
          await interaction.response.send_message(totach,ephemeral=True)

      else:
        if self.T3P == '⚫':
          self.T3P = '🟢'
          
          await self.apdate_embed(interaction)
        else:
          await interaction.response.send_message(totach,ephemeral=True)
    else:
      await interaction.response.send_message('Вы не состоите в команде',
                                              ephemeral=True)
        
      


  @discord.ui.button(label='Lose', style=discord.ButtonStyle.red)
  async def lose(self, button, interaction):
    totach = "Вы уже нажали на кнопку"
    if interaction.user.id in self.list_team:
      if interaction.user.id == self.AuthorID:
        if self.AuP == '⚫':
          self.AuP = '🔴'
          await self.apdate_embed(interaction)
        else:
          await interaction.response.send_message(totach,ephemeral=True)

      elif interaction.user.id == self.Team1ID:
        if self.T1P == '⚫':
          self.T1P = '🔴'
          
          
          await self.apdate_embed(interaction)
        else:
          await interaction.response.send_message(totach,ephemeral=True)

      elif interaction.user.id == self.Team2ID:
        if self.T2P == '⚫':
          self.T2P ='🔴'
          
          
          await self.apdate_embed(interaction)
        else:
          await interaction.response.send_message(totach,ephemeral=True)

      else:
        if self.T3P == '⚫':
          self.T3P = '🔴'
          
          
          await self.apdate_embed(interaction)
        else:
          await interaction.response.send_message(totach,ephemeral=True)
    
    else:
      await interaction.response.send_message('Вы не состоите в команде',
                                              ephemeral=True)


  @discord.ui.button(label='remove')
  async def remove(self, button, interaction):
    if interaction.user.id in self.list_team:
      if interaction.user.id == self.AuthorID:
        self.AuP = '⚫'
        await self.apdate_embed(interaction)
      elif interaction.user.id == self.Team1ID:
        self.T1P = '⚫'
        await self.apdate_embed(interaction)
      elif interaction.user.id == self.Team2ID:
        self.T2P = '⚫'
        await self.apdate_embed(interaction)
      else:
        self.T3P = '⚫'
        await self.apdate_embed(interaction)
    else:
      await interaction.response.send_message('Вы не состоите в команде',ephemeral=True)
  
  





    
    









class button2v2View(View):

  def __init__(self, ctx, collection,Author, *args, **kwargs):
    # Передайте игрока в качестве аргумента конструктору
    super().__init__(*args, **kwargs, timeout=600)
    self.ctx = ctx
    self.collection = collection
    self.Author = Author
    
    
    self.DontAgain = 'Вы уже состоите в команде'
    self.PlzReg="Вы не зарегестрированы.\nДля регестрации воспользуйтесь коммандой /reg"

    
    self.join1press = False
    self.join2press = False
    self.join3press = False
    self.FreeTeam2 = True


    self.AuthorID = ctx.author.id
    self.Team1ID = None
    self.Team2ID = None
    self.Team3ID = None
    self.list_team = [ctx.author.id]


    
    self.AuthorN = Author['EA_Name']
    self.AuthorR = Author['Rating_2v2']
    self.Team1N = '___'
    self.Team1R = 0
    self.Team2N = '___'
    self.Team2R = 0
    self.Team3N = '___'
    self.Team3R = 0

  async def game_start(self, interaction):
    view2 = Rating_2v2(self.ctx, self.collection,interaction,
     self.AuthorID,self.Team1ID, self.Team2ID, self.Team3ID,
     self.list_team,
     self.Team1N,self.Team1R,                       
     self.Team2N,self.Team2R,
     self.Team3N,self.Team3R,
     self.AuthorN,self.AuthorR
    )
    await interaction.response.edit_message(view=view2)
    

  async def apdate_embed(self,interaction):
    # Функция для обновления сообщения с информацией о команде
    current_embed = interaction.message.embeds[0]
    
    current_embed.set_field_at(1,name=f"`{self.AuthorR+self.Team1R}`",
       value=f"`{self.AuthorN}`\n`{self.Team1N}`",inline=True)
  
  
    current_embed.set_field_at(2, name=f"`{self.Team2R+self.Team3R}`",
       value=f"`{self.Team2N}`\n`{self.Team3N}`",inline=True)

    if self.join1press and self.join2press and self.join3press:
      await self.game_start(interaction)
    else:
      await interaction.response.edit_message(embed=current_embed,view=self)

   
      
    
  @discord.ui.button(label="join",style=discord.ButtonStyle.grey,row=2,custom_id="join1")
  async def join1(self,button,interaction):
    check_author = self.collection.find_one({"_id": str(interaction.user.id)})
    # Проверяем. Существует ли человек в нашей базе данных
    if check_author:
      # Человек найден. Проверяем состоит ли он уже в команде или нет.
      if interaction.user.id in self.list_team:
        await interaction.response.send_message(self.DontAgain,ephemeral=True)
      else:
        # Отключаем кнопку и запоминаем игрока
        
        self.Team1ID = interaction.user.id
        self.join1press = True
        button.disabled = True
        # Добавляем игрока в список играков что присоеденились
        self.Team1N = check_author['EA_Name']
        self.Team1R = check_author['Rating_2v2']
        self.list_team.append(interaction.user.id)
        
        button.disabled = True
        # Запускаем функцию обновления сообщения
        await self.apdate_embed(interaction)
    else:
      await interaction.response.send_message(self.PlzReg,ephemeral=True)






  @discord.ui.button(label="join",style=discord.ButtonStyle.blurple,row=2,custom_id="join2")
  async def join2(self,button,interaction):
    check_author = self.collection.find_one({"_id": str(interaction.user.id)})
    if check_author:
      if interaction.user.id in self.list_team:
        await interaction.response.send_message(self.DontAgain,ephemeral=True)
      else:
        if self.FreeTeam2:
          self.FreeTeam2 = False
          self.join2press = True
          
          self.Team2N = check_author['EA_Name']
          self.Team2R = check_author['Rating_2v2']
          self.Team2ID = interaction.user.id
          self.list_team.append(interaction.user.id)
          await self.apdate_embed(interaction)
          if self.join3press:
            button.disabled = True
        else:
          self.Team3N = check_author['EA_Name']
          self.Team3R = check_author['Rating_2v2']
          self.Team3ID = interaction.user.id
          self.list_team.append(interaction.user.id)
          self.join3press = True
          if self.join2press:
            button.disabled = True
    
          await self.apdate_embed(interaction)

    else:
      await interaction.response.send_message(self.PlzReg,ephemeral=True)

  @discord.ui.button(label="exit",style=discord.ButtonStyle.red,row=2)
  async def exit(self,button,interaction):
    if interaction.user.id in self.list_team:
      self.list_team.remove(interaction.user.id)
      if interaction.user.id == self.Team1ID:
        self.Team1ID = None
        self.Team1N = '___'
        self.Team1R = 0
        self.join1press = False
        join1_button = [btn for btn in self.children if btn.custom_id == "join1"][0]
        join1_button.disabled = False
        await self.apdate_embed(interaction)

      elif interaction.user.id == self.Team2ID:
        self.Team2ID = None
        self.Team2N = '___'
        self.Team2R = 0
        self.FreeTeam2 = True
        self.join2press = False
        
        join1_button = [btn for btn in self.children if btn.custom_id == "join2"][0]
        join1_button.disabled = False
        await self.apdate_embed(interaction)

      elif interaction.user.id == self.Team3ID:
        self.Team3ID = None
        self.Team3N = '___'
        self.Team3R = 0
        self.join3press = False
        join1_button = [btn for btn in self.children if btn.custom_id == "join2"][0]
        join1_button.disabled = False
        
        await self.apdate_embed(interaction)

      elif interaction.user.id == self.AuthorID:
        try:
          await interaction.message.delete()
          await interaction.response.send_message('Вызов удален',ephemeral=True)
        except discord.NotFound:
          await interaction.response.send_message('Вызов уже удален',ephemeral=True)
        except discord.Forbidden:
          await interaction.response.send_message(
            "У меня нет прав на удаление этого сообщения.", ephemeral=True)
      else:
        await interaction.response.send_message('Вас больше нет в списке',
                                                ephemeral=True)
        
    else:
      await interaction.response.send_message('Вы не состоите в команде',
                                              ephemeral=True)
    
    
  
  






