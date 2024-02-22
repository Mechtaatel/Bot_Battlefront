import discord
from discord.ui import Button, View
import json

class check_role():
  def __init__(self, ctx, collection, Dictionaries_Team):
    if Dictionaries_Team == 0:
      return
    else:
      for kye, value in Dictionaries_Team.items():
        if value['id']:
          lose = 1
  