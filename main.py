import logging
import os
import json

import discord
from discord.ext import commands
from discord.ui import Button, View, Select
from discord.utils import get

from Rating_commands.rating_check import Rating_Role
from Rating_commands.v1 import button1v1View
from Rating_commands.v2 import button2v2View
from Rating_commands.v4 import button4v4View

from Rating_commands.v1byhand import v1byhand

#Twitch тема:

from Other_commands.switch import role_commands
#from Rating_commands.reg import check_name_and_reg

import pymongo
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient

intents = discord.Intents.all()
intents.members = True
intents.typing = False
intents.presences = False

bot = discord.Bot(intents=intents)

# guild
settings = 'Main'

if settings == 'Main':

  guild_id = 1071600435607113819
  token = os.environ['token']

  # Role
  rating_0 = 1165749431455461437
#channel
elif settings == 'Test':
  guild_id = 1142846260454375434
  token = os.environ['token_test']
  # Role
  rating_0 = 1142846260504707143

#role
# r_forse_s = 1142846260521472054

# Создайте нового клиента и подключитесь к серверу
client = MongoClient(os.environ['mongo'])

db = client.get_database('Rating_data_base')
collection = db['Collection_data']
# Отправьте пинг, чтобы подтвердить успешное соединение

try:
  client.admin.command('ping')
  print("Пропинговал ваше развертывание. Вы успешно подключились к MongoDB!")
except Exception as e:
  print(e)


@bot.event
async def on_ready():
  print(f"{bot.user} is ready and online!")


# Ниже представлен обработчик ошибок
# @bot.event
# async def on_command_error(ctx, error):
#   if isinstance(error, commands.MissingPermissions):
#     missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
#     if len(missing) > 2:
#         fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
#     else:
#         fmt = ' and '.join(missing)
#     _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
#     await ctx.send(_message)
#     return

# async def on_command_error(ctx, error):
#   # Попытка выполнить команду человеком что не имеет на это право.
#   if isinstance(error, commands.MissingPermissions):
#     await ctx.send('У вас недостаточно прав для этого!')
#     print(f'{ctx.author} Попытался выполнить команду {ctx.message.content}')

# Для других типов ошибок вы можете добавить сюда дополнительную логику обработки.


@bot.event
async def on_member_join(member):
  check_author = collection.find_one({"_id": str(member.id)})
  guild = member.guild  # Получить сервер, к которому присоединился участник
  if guild.id == guild_id:
    # Добавляем роль только что присоединившемуся участнику
    role = guild.get_role(rating_0)
    await member.add_roles(role)
    channel = guild.get_channel(1071600437209354241)
    if check_author:
      await channel.send(f'С возвращением, {member.mention}!')
    else:
      await member.send(
  f"""Привет, {member.mention}!
Добро пожаловать на сервер. Пройдите регистрацию коммандой /reg.
В пункте name Укажите свой никнейм из EA, в пункте hourse укажите время проведеннное в игре."""
      )
      await channel.send(f'Поприветсвуем нового участника, {member.mention}!')
    
    
  else:
    print('Не работает')

  #channel = guild.get_channel(1142846261196759071)
  # Замените YOUR_WELCOME_CHANNEL_ID фактическим идентификатором канала, на котором вы
  #хотите отправить приветственное сообщение
  #await channel.send(f'Welcome to the server, {member.mention}!')
  # Отправьте приветственное сообщение на указанный канал


# Для нашего удобства давайте создадим функцию
def parse_embed_json(json_file):
  embeds_json = json.loads(json_file)['embeds']

  for embed_json in embeds_json:
    embed = discord.Embed.from_dict(embed_json)
    yield embed






    

@bot.command(name='say', description='Отправить сообщение от имени бота')
@commands.has_permissions(administrator=True)
async def say(ctx, message):

  try:
    print(f'{ctx.author} использовал команду /say')
    await ctx.send(message)
    # Do something with the argument.
    ...
  except Exception as e:
    # Handle the error and provide a custom error message.
    await ctx.send(f"An error occurred: {e}")
  



# И основной код выглядит так
@bot.command(name='embed', description='Отправить embed сообщение')
@commands.has_permissions(administrator=True)
async def add_embend(ctx, name: str):
  if name == 'help':
    with open("embed/help.json", "r") as file:
      temp_ban_embeds = parse_embed_json(file.read())

    for embed in temp_ban_embeds:
      await ctx.send(embed=embed)


@bot.command(name='rating', description='Узнать свой рейтинг')
async def rating(ctx):
  member = ctx.user
  check_author = collection.find_one({"_id": str(member.id)})
  if check_author:
    await ctx.respond(
        f"""Режим 4 на 4:`{check_author['Rating_4v4']}`
Режим 2 на 2:`{check_author['Rating_2v2']}`
Режим 1 на 1:`{check_author['Rating_1v1']}`""")
  else:
    await ctx.respond('Вы не зарегистрированы')



@bot.command(name='help', description='список команд')
async def help(ctx):
  await ctx.respond("https://discord.com/channels/1071600435607113819/")


@bot.command(name='name', description='Узнать nickname участника')
async def name(ctx, member: discord.Member):
  check_author = collection.find_one({"_id": str(member.id)})
  if check_author:
    await ctx.respond(f"`{check_author['EA_Name']}`")
  else:
    await ctx.respond(f'Участник `{member.name}` не зарегистрирован')


@bot.command()
@commands.has_permissions(administrator=True)
async def reup(ctx,member: discord.Member):
  db = client.get_database('Rating_data_base')
  collection = db['Collection_data']
  intcollecion = collection.find_one({"_id"})
  print(intcollecion)
  


@bot.command(name='reg_byhand', description='Регистрация пользоваетля в ручную')
@commands.has_permissions(administrator=True)
async def regbyhand(ctx, name: str, rating: int, member: discord.Member):
  
  db = client.get_database('Rating_data_base')
  collection = db['Collection_data']
  # listdb_users = db.Rating_data_base.find({})
  # list_db_users = list(listdb_users)
  # idUsers = list_db_users[0]

  # Создаем запрос в MongoDB для поиска пользователя по id.
  user_document = collection.find_one({"_id": str(member.id)})

  # Проверяем найден ли id пользователя в базе данных
  if user_document:
    # Получить доступ к `EA_Name` непосредственно из `user_document`
    EAName = user_document['EA_Name']
    await ctx.respond(
      f'Пользователь уже зарегестрированы под никнемом {EAName}.')

  else:

    #async def check_name_in_database(ctx,db, name):
    # Проверяем найден ли name пользователя в базе данных
    user_document1 = collection.find_one({"EA_Name": name})
    if user_document1:
      await ctx.respond(f"Имя {name} уже занято пользователем")
      return
    else:
      guild = bot.get_guild(guild_id)
      roles = member.roles
      role = roles[len(roles) - 1]

      with open('Rating_commands/Role.json','r') as f:
        vipRole = json.load(f)
      
      if role.id == 1197490336075890718:
        role = roles[len(roles) - 2]
      elif role.id not in vipRole['VIP']: 
        await member.remove_roles(role)
        await member.add_roles(guild.get_role(1071604948476895263))
  
      new_data = {
          'EA_Name': name,
          'Rating_1v1': rating,
          'Rating_2v2': rating,
          'Rating_4v4': rating,
          'Ban': 'off'
      }

      collection.update_one({'_id': str(member.id)}, {"$set": new_data}, upsert=True)
      await ctx.respond(f"Пользоваетль {member} зарегестрирован.")
      


@bot.command(name='switche', description='')
async def switch(ctx, role: str):

  check_author = collection.find_one({"_id": str(ctx.author.id)})
  if check_author:
    if role == 'Light':
      await ctx.respond('Вернуться уже не получится)'
                                                  )
    guild = bot.get_guild(guild_id)
    obj = role_commands(ctx, check_author, guild, role)
    await obj.switch()
  else:
    await ctx.respond(
        'Вы не зарегестрированы, воспользуйтесь командой /reg')


@bot.command(description="""Регистрация. В пункте Name: введите свой ник.
    В пункте hourse введите сколько у вас часов""")
async def reg(ctx, name: str, hourse: int):
  if hourse <= 50:
    rating = 200
  elif hourse <= 300:
    rating = 400
  elif hourse <= 4000:
    rating = 600
  else:
    rating = 1000

  db = client.get_database('Rating_data_base')
  collection = db['Collection_data']
  # listdb_users = db.Rating_data_base.find({})
  # list_db_users = list(listdb_users)
  # idUsers = list_db_users[0]

  # и `user_id` это id пользователя (ctx.author.id)

  # преобразуем в строку, поскольку в JSON ключи являются строками
  user_id = str(ctx.author.id)
  # Создаем запрос в MongoDB для поиска пользователя по id.
  user_document = collection.find_one({"_id": user_id})

  # Проверяем найден ли id пользователя в базе данных
  if user_document:
    # Получить доступ к `EA_Name` непосредственно из `user_document`
    EAName = user_document['EA_Name']
    await ctx.respond(
        f'Вы уже зарегестрированы под никнемом {EAName}.')

  else:

    #async def check_name_in_database(ctx,db, name):
    # Проверяем найден ли name пользователя в базе данных
    user_document1 = collection.find_one({"EA_Name": name})
    if user_document1:
      await ctx.respond(
          f"""Имя {name} уже занято пользователем.
Обратитесь пожалуйста в Администрацию.""")
      return
    else:
      guild = bot.get_guild(guild_id)
      member = ctx.user
      roles = member.roles
      role = roles[len(roles) - 1]

      with open('Rating_commands/Role.json','r') as f:
        vipRole = json.load(f)
      if role.id == 1197490336075890718:
        role = roles[len(roles) - 2]
      elif role.id not in vipRole['VIP']: 
        await member.remove_roles(role)
        await member.add_roles(guild.get_role(1071604948476895263))
        

      new_data = {
          'EA_Name': name,
          'Rating_1v1': rating,
          'Rating_2v2': rating,
          'Rating_4v4': rating,
          'Ban': 'off'
      }

      collection.update_one({'_id': user_id}, {"$set": new_data}, upsert=True)
      await ctx.respond(
"""Поздравляем вы зарегестрированы. Воспользуйтесь командой /help что бы узнать основные команды."""
      )
      

@bot.command(description='Вызвать в игру 4 на 4')
async def v4(ctx):
  check_author = collection.find_one({"_id": str(ctx.author.id)})
  if check_author:
    guild = bot.get_guild(guild_id)
    AuthorMG = check_author
    embed = discord.Embed(
        title='',
        description=
        f'Игрок <@{ctx.author.id}> начинает поиск игроков в режим 4 на 4',
        color=0x1c2951)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name=f"`{AuthorMG['Rating_4v4']}`",
                    value=f"`{AuthorMG['EA_Name']}`\n`___`\n`___`\n`___`",
                    inline=True)
    embed.add_field(name="`0`",
                    value="`___`\n`___`\n`___`\n`___`",
                    inline=True)
    embed.set_footer(text="")
    view = button4v4View(ctx, collection, AuthorMG, guild)
    await ctx.respond('<@&1167993718704447519>.',
                                                embed=embed,
                                                view=view)
  else:
    await ctx.respond(
        """Вы не зарегестрированы.\nДля регестрации воспользуйтесь коммандой /reg"""
    )


@bot.command(description='Вызвать в игру 2 на 2')
async def v2(ctx):
  check_author = collection.find_one({"_id": str(ctx.author.id)})
  if check_author:
    guild = bot.get_guild(guild_id)
    AuthorMG = collection.find_one({"_id": str(ctx.author.id)})
    embed = discord.Embed(
        title='',
        description=
        f'Игрок <@{ctx.author.id}> начинает поиск игроков в режим 2 на 2',
        color=0x1c2951)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name=f"`{AuthorMG['Rating_2v2']}`",
                    value=f"`{AuthorMG['EA_Name']}`\n`___`",
                    inline=True)
    embed.add_field(name="`0`", value="`___`\n`___`", inline=True)
    embed.set_footer(text="")
    view = button2v2View(ctx, collection, AuthorMG, guild)
    await ctx.respond('<@&1167993718704447519>.',
                                                embed=embed,
                                                view=view)
  else:
    await ctx.respond(
        """Вы не зарегестрированы.\nДля регестрации воспользуйтесь коммандой /reg"""
    )





@bot.command(description="Ручной ввод.")
@commands.has_permissions(administrator=True)
async def v1byhend(ctx, member_1: discord.Member, member_2: discord.Member):
  db = client.get_database('Rating_data_base')
  collection = db['Collection_data']
  
  member1db = collection.find_one({"_id": str(member_1.id)})
  member2db = collection.find_one({"_id": str(member_2.id)})

  if member1db:
    if member_1.id == member_2.id:
      await ctx.respond(
          'Вы не можете вызвать самого себя')
    else:
      if member2db:
        guild = bot.get_guild(guild_id)
        view = v1byhand(ctx, member_1.id,member_2.id, db, guild)
        await ctx.respond(
            f'Игрок {member_1} против {member_2}',view=view)
      else:
        await ctx.respond(
          f'Игрок {member_2} не зарегестрирован')
  else:
    await ctx.respond(f"Игрок {member_1} не зарегестрирован")





@bot.command(description="Вызов на дуэль.")
async def v1(ctx, member: discord.Member):
  db = client.get_database('Rating_data_base')
  collection = db['Collection_data']

  check_author = collection.find_one({"_id": str(ctx.author.id)})
  user_document = collection.find_one({"_id": str(member.id)})

  if check_author:
    if member.id == 1150018596307734579:
      await ctx.respond(
          'Я не думаю что ты способен победить меня xd')
    # Запускаем класс с кнопками если все прекрастно
    elif ctx.author.id == member.id:
      await ctx.respond(
          'Вы не можете вызвать самого себя')
    else:
      if user_document:
        guild = bot.get_guild(guild_id)
        view = button1v1View(ctx, member.id, db, guild)
        await ctx.respond(
            f'Вызов на столкновение игрока <@{member.id}> (`{user_document["Rating_1v1"]}`)',
            view=view)

      else:
        await ctx.respond(
            'Этот игрок не зарегестрирован.')
  else:
    await ctx.respond(
        """Вы не зарегестрированы.\nДля регестрации воспользуйтесь коммандой /reg"""
    )


# @bot.command()
# @commands.has_permissions(administrator=True)

bot.run(token)
