import discord
from discord.ui import Button, View
import pymongo
import json
import math
from Rating_commands.rating_check import Rating_Role
 
  

class v1byhand(discord.ui.View):
  def __init__(self,ctx,player_1,player_2,db, guild):
    super().__init__(timeout=600)
    self.ctx = ctx
    self.player_1 = player_1
    self.player_2 = player_2
    self.loseU = None
    self.winU = None
    self.db = db
    self.guild = guild



  @discord.ui.button(label="Reapet", style=discord.ButtonStyle.green)
  async def repeat(self,button,interaction):
    if interaction.user.id == int(self.ctx.author.id):

      self.remove_item(self.repeat)
      self.remove_item(self.close)

      self.add_item(self.win)
      self.add_item(self.lose)

      await interaction.response.edit_message(view=self)
      

  @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
  async def close(self,button,interaction):
    if interaction.user.id == int(self.ctx.author.id):
      await interaction.response.edit_message(view=None)

  

  
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


    R_a = A + K_a * (S_a - E_a)
    R_b = B + K_b * (S_b - E_b)

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
    Dictionaries_Team = {'op1':{'id': int(self.winU)}, 'op': {'id': int(self.loseU)}}
    try:
      # Try to edit the original message if response already sent
      
      Rating_Role(self.ctx, collection, Dictionaries_Team,self.guild)
      self.remove_item(self.win)
      self.remove_item(self.lose)
      self.add_item(self.repeat)
      self.add_item(self.close)
      await interaction.edit_original_response(content=
                                              f"""
Победитель: <@{self.winU}> (`{R_a}`) | Пороигравший: <@{self.loseU}> (`{R_b}`)""",
                                                view=self
                                                )
    except discord.errors.InteractionResponded:
      print('Error')


  @discord.ui.button(label='Win', style=discord.ButtonStyle.green)
  async def win(self, button, interaction):
    if self.loseU:
      self.winU = str(self.player_2)
    else:
      self.winU = str(self.player_1)
    button.disabled = True
    await interaction.response.edit_message(view=self)
    if self.winU and self.loseU:
      await self.perform_both_button_pressed_action(interaction)



  @discord.ui.button(label='Lose', style=discord.ButtonStyle.red)
  async def lose(self, button, interaction):
    if self.winU:
      self.loseU = str(self.player_2)
    else:
      self.loseU = str(self.player_1)
    button.disabled = True
    await interaction.response.edit_message(view=self)
    if self.winU and self.loseU:
      await self.perform_both_button_pressed_action(interaction)
  
        

  async def on_timeout(self):
    for ithem in self.children:
      if isinstance(ithem, discord.ui.Button):
        ithem.disabled = True
      await self.ctx.edit_message(view=self)
  


