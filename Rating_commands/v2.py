import discord
from discord.ui import Button, View
import json
import math



class Rating_2v2(View):
  def __init__(self, ctx, collection,
               Author,
               summ_rating_team1,
               summ_rating_team2,
               team_1,
               team_2_1,
               team_2_2
              ):
    super().__init__(timeout=3600)
    self.ctx = ctx
    self.collection = collection
    self.Author = Author
    self.summ_rating_team1 = summ_rating_team1
    self.summ_rating_team2 = summ_rating_team2
    self.team_1 = team_1
    self.team_2_1 = team_2_1
    self.team_2_2 = team_2_2
    

  

  

  

  

    
  @discord.ui.button(label='Win', style=discord.ButtonStyle.green)
  async def win(self, button, interaction):
    # Проверяем что бы нажимали именно участники.
    if interaction.user == self.Author:
      current_embed = interaction.message.embeds[0]
      current_embed.set_field_at(1,name=f"`{self.summ_rating_team1}`",
         value=f"`{self.AuthorN}`\n`{check_author['EA_Name']}`",inline=True)





    


  




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









class button2v2View(View):

  def __init__(self, ctx, collection,Author, *args, **kwargs):
    # Передайте игрока в качестве аргумента конструктору
    super().__init__(*args, **kwargs, timeout=600)
    self.ctx = ctx
    self.collection = collection
    self.AuthorN = Author['EA_Name']
    self.AuthorR = Author['Rating_2v2']

    self.DontAgain = 'Вы уже состоите в команде'
    self.PlzReg="Вы не зарегестрированы.\nДля регестрации воспользуйтесь коммандой /reg"

    
    self.FreeTeam2 = True
    self.team_1 = None
    self.team_2_1 = None
    self.team_2_2 = None
    self.list_team = [ctx.author.id]


  
  
  @discord.ui.button(label="join", style=discord.ButtonStyle.grey,row=2)
  async def join1(self,button,interaction):
    # Проверяем не пытается ли афтор добавить самого себя в команду
    if interaction.user.id == self.ctx.author.id:
      await interaction.response.send_message(self.DontAgain,ephemeral=True)

    else:
      check_author = self.collection.find_one({"_id": str(interaction.user.id)})
      # Проверяем. Существует ли человек в нашей базе данных
      if check_author:
        q = 0
        # Человек найден. Проверяем состоит ли он уже в команде или нет.
        for i in self.list_team:
          if i != interaction.user.id:
            q += 1
            # Функция len() возвращает количество элементов в списке
            if q == len(self.list_team):
              # Человек не состоит ни в одной из команд а значит мы его добовляем:

              # Сумма рейтинга первой команды
              summ_rating_team1 = self.AuthorR + check_author['Rating_2v2']
              self.summ_rating_team1 = summ_rating_team1

              # Изменяем Ембенд
              current_embed = interaction.message.embeds[0]
              current_embed.set_field_at(1,name=f"`{summ_rating_team1}`",
                                           value=f"`{self.AuthorN}`\n`{check_author['EA_Name']}`",inline=True)


              # Отключаем кнопку и запоминаем игрока
              button.disabled = True
              self.team_1 = interaction.user.id
              


              # Удаляем рудимент в виде 1
              # if 1 in self.list_team:
              #   self.list_team.remove(1)

              # Добавляем игрока в список играков что присоеденились
              self.list_team.append(interaction.user.id)
              
              
              await interaction.response.edit_message(embed=current_embed,view=self)
              
          elif i == interaction.user.id:
            await interaction.response.send_message(self.DontAgain,ephemeral=True)
              
              
            
                
      else:
        await interaction.response.send_message(self.PlzReg,ephemeral=True)



  
  
  
  @discord.ui.button(label="join",style=discord.ButtonStyle.blurple,row=2)
  async def join2(self,button,interaction):
    
    
    if interaction.user.id == self.ctx.author.id:
      await interaction.response.send_message(self.DontAgain,ephemeral=True)

    else:
      # Первая команда работает. Сделай так же и эту.
      check_author = self.collection.find_one(
      {"_id": str(interaction.user.id)}
      )
      if check_author:
        q = 0
        for i in self.list_team:
          if i != interaction.user.id:
            q += 1
            if q == len(self.list_team):
              if self.FreeTeam2:
                current_embed = interaction.message.embeds[0]
                current_embed.set_field_at(2, name=f"`{check_author['Rating_2v2']}`",
                                           value=f"`{check_author['EA_Name']}`\n`___`",
                                            inline=True
                                            )
                self.team2 = check_author['EA_Name']
                self.team2r = check_author['Rating_2v2']
                self.FreeTeam2 = False


                
                self.team_2_1 = interaction.user.id
                
                
                await interaction.response.edit_message(embed=current_embed,view=self)
              else:
                summ_rating_team2 = self.team2r + check_author['Rating_2v2']
                self.summ_rating_team2 = summ_rating_team2
                current_embed = interaction.message.embeds[0]
                current_embed.set_field_at(2, name=f"`{summ_rating_team2}`",
                                           value=f"`{self.team2}`\n`{check_author['EA_Name']}`",
                                            inline=True
                                            )

                button.disabled = True
                
                self.team_2_2 = interaction.user.id
                self.list_team.append(interaction.user.id)
                
                await interaction.response.edit_message(embed=current_embed,view=self)
                
              
          elif i == interaction.user.id:
            await interaction.response.send_message(self.DontAgain,ephemeral=True)
          
      else:
        await interaction.response.send_message(self.PlzReg,ephemeral=True)
      
      






