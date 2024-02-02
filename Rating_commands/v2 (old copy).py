import discord
from discord.ui import Button, View
import json
import math




class button2v2View(View):

  def __init__(self, ctx, collection, *args, **kwargs):
    # Передайте игрока в качестве аргумента конструктору
    super().__init__(*args, **kwargs, timeout=600)
    self.ctx = ctx
    self.collection = collection
    # Сохраняем игрока в переменную self.player вместо player
    Author = self.collection.find_one({"_id": str(ctx.author.id)})

    self.add_item(discord.ui.Button(label=f"{Author['EA_Name']}",
                                    style=discord.ButtonStyle.primary, 
                                    custom_id = "1.0",
                                    row=0
                                    ))
    self.add_item(discord.ui.Button(label="___",
                                    style=discord.ButtonStyle.primary,
                                    custom_id = "1.1",
                                    row=1)
                 )
    self.add_item(discord.ui.Button(label="___",
                                    style=discord.ButtonStyle.secondary,
                                    custom_id = "2.0",
                                    row=0
                                   ))
    self.add_item(discord.ui.Button(label="___",
                                    style=discord.ButtonStyle.secondary,
                                    custom_id = "2.1",
                                    row=1
                                   ))
    
    
    
    self.team_press = False
    self.list_u = [0]
  
  
  @discord.ui.button(label="join", style=discord.ButtonStyle.grey,row=2)
  async def join1(self,button,interaction):
    # Проверяем не пытается ли афтор добавить самого себя в команду
    if interaction.user.id == self.ctx.author.id:
      await interaction.response.send_message("Вы уже состоите в команде",
                                              ephemeral=True)

    else:
      check_author = self.collection.find_one({"_id": str(interaction.user.id)})
      # Проверяем. Существует ли человек в нашей базе данных
      if check_author:
        q = 0
        # Человек найден. Проверяем состоит ли он уже в команде или нет.
        for i in self.list_u:
          if i != interaction.user.id:
            q += 1
            if q == len(self.list_u):
              # Человек не состоит ни в одной из команд а значит мы его добовляем:
              for ithem in self.children:
                if isinstance(ithem, discord.ui.Button) and ithem.custom_id == "1.1":

                  button.disabled = True
                  ithem.label = f"{check_author['EA_Name']}"
                  self.list_u.append(interaction.user.id)
                  await interaction.response.edit_message(view=self)
              
            elif i == interaction.user.id:
              await interaction.response.send_message('Вы уже состоите в команде',
                ephemeral=True)
              
              
            
                
      else:
        await interaction.response.send_message("Вы не зарегестрированы.\nДля регестрации воспользуйтесь коммандой /reg",
                                                    ephemeral=True)
  
  @discord.ui.button(label="join", style=discord.ButtonStyle.blurple,row=2)
  async def join2(self,button,interaction):
    if interaction.user.id == self.ctx.author.id:
      await interaction.response.send_message("Вы уже состоите в команде",
                                              ephemeral=True)

    else:
      # Первая команда работает. Сделай так же и эту.
      check_author = self.collection.find_one(
      {"_id": str(interaction.user.id)}
      )
      if check_author:
        q = 0
        for i in self.list_u:
          if i != interaction.user.id:
            q += 1
        if q == 3:
          if self.team_press:
            for ithem in self.children:
              if isinstance(ithem, discord.ui.Button) and ithem.custom_id == "2.0":
                self.team_10_press = True
                ithem.label = f"{check_author['EA_Name']}"
                await interaction.response.edit_message(view=self)
            
          else:
            for ithem in self.children:
              if isinstance(ithem, discord.ui.Button) and ithem.custom_id == "2.1":
                self.team_10_press = True
                ithem.label = f"{check_author['EA_Name']}"
                await interaction.response.edit_message(view=self)
        else:
            await interaction.response.send_message('Вы уже состоите в команде',
                                                            ephemeral=True)
      else:
        await interaction.response.send_message("Вы не зарегестрированы.\nДля регестрации воспользуйтесь коммандой /reg",
                                                    ephemeral=True)
      
      





