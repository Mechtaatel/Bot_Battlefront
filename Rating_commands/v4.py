import discord
from discord.ui import Button, View
import json
import os

from pymongo import MongoClient

client = MongoClient(os.environ['mongo'])

db =client['Rating_data_base']
print(db)