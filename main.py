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

  guild = member.guild  # Получить сервер, к которому присоединился участник
  if guild.id == guild_id:
    role = guild.get_role(rating_0)
    await member.add_roles(role)
  # Добавляем роль только что присоединившемуся участнику
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
      f"Режим 4 на 4:`{check_author['Rating_4v4']}`\nРежим 2 на 2:`{check_author['Rating_2v2']}`\nРежим 1 на 1:`{check_author['Rating_1v1']}`")
  else:
    await ctx.respond(f'Вы не зарегистрированы')


  

@bot.command(name='name', description='Узнать nickname участника')
async def name(ctx, member: discord.Member):
  check_author = collection.find_one({"_id": str(member.id)})
  if check_author:
    await ctx.respond(f"`{check_author['EA_Name']}`")
  else:
    await ctx.respond(f'Участник `{member.name}` не зарегистрирован')

def sll(check_author):
  sl = [
      check_author['Rating_1v1'], check_author['Rating_2v2'],
      check_author['Rating_4v4']
  ]

  for i in range(2):
    for j in range(3 - i - 1):
      if sl[j] < sl[j + 1]:
        sl[j], sl[j + 1] = sl[j + 1], sl[j]
  return sl


def levelR(r, l):
  if r > 1200:
    r -= 400
    l += 1
    return levelR(r, l)
  else:
    return l


async def check_level(ctx, Roles, role, member, guild, level):
  if role.id in Roles['VIP']:
    return 'V'
  elif role in Roles['L']:
    if level == Roles['L'].index(role.id):
      return 'L-0'
    else:
      return 'L'
  elif role.id in Roles['D']:
    if level == Roles['D'].index(role.id):
      return 'D-0'
    else:
      return 'D'
  elif role.id in Roles['M']:
    return 'M'
  elif role.id == Roles['O']:

    await member.remove_roles(role)
    await member.add_roles(guild.get_role(Roles['L'][0]))
    await ctx.respond("Ваша роль обнавлена")


@bot.command()
async def switch(ctx, role: str):

  check_author = collection.find_one({"_id": str(ctx.author.id)})
  if check_author:

    sl = sll(check_author)
    level = levelR(sl[0], 0)

    with open('Role.json') as f:
      Roles = json.load(f)
    if role == 'Dark':
      roleid = 1071606225189470339
    elif role == 'Mando':
      roleid = 1073721742406713426
    else:
      await ctx.send('Error')
      return
    member = ctx.user

    roles = member.roles
    role1 = roles[len(roles) - 1]
    for i in Roles.keys():

      if roleid in Roles[i] and role1.id in Roles[i]:
        await ctx.send('Вам не требуется смена роли')
        return
      elif roleid in Roles[i] and role1.id not in Roles[i]:
        if i == 'D':
          guild = bot.get_guild(guild_id)
          await member.remove_roles(role1)
          await member.add_roles(guild.get_role(Roles[i][level]))
          await ctx.respond("Ваша роль обнавлена")
          return
        elif i == 'M':
          await member.remove_roles(role1)
          await member.add_roles(guild.get_role(Roles[i][0]))
          await ctx.respond("Ваша роль обнавлена")
          return

  else:
    await ctx.respond('Вы не зарегестрированы, воспользуйтесь командой /reg')


@bot.command()
async def roleup(ctx):

  check_author = collection.find_one({"_id": str(ctx.author.id)})

  if check_author:
    sl = sll(check_author)
    level = levelR(sl[0], 0)

    with open('Role.json') as f:
      Roles = json.load(f)

    member = ctx.user
    guild = bot.get_guild(guild_id)
    roles = member.roles
    role = roles[len(roles) - 1]
    side = await check_level(ctx, Roles, role, member, guild, level)
    if side == 'V' or side == 'M':
      await ctx.respond('Вы не нуждаетесь в обновлении роли')
    elif side == "L-0" or side == "D-0":
      await ctx.respond('Ваша роль соответствует вашему уровню')
    elif side == "L" or side == "D":

      await member.remove_roles(role)
      await member.add_roles(guild.get_role(Roles[side][level]))
      await ctx.respond('Ваша роль обновлена')

  else:
    await ctx.respond('Вы не зарегестрированы, воспользуйтесь командой /reg',
                      ephemeral=True)


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
    await ctx.respond(f'Вы уже зарегестрированы под никнемом {EAName}.')

  else:

    #async def check_name_in_database(ctx,db, name):
    # Проверяем найден ли name пользователя в базе данных
    user_document1 = collection.find_one({"EA_Name": name})
    if user_document1:
      await ctx.respond(
          f"""Имя {name} уже занято пользователем.\nОбратитесь пожалуйста в Администрацию."""
      )
      return ()
    else:
      with open('Role.json') as f:
        Roles = json.load(f)
      guild = bot.get_guild(guild_id)
      member = ctx.user
      roles = member.roles
      role = roles[len(roles) - 1]
      await member.remove_roles(role)
      await member.add_roles(guild.get_role(Roles['L'][0]))

      new_data = {
          'EA_Name': name,
          'Rating_1v1': rating,
          'Rating_2v2': rating,
          'Rating_4v4': rating,
          'Ban': 'off'
      }

      collection.update_one({'_id': user_id}, {"$set": new_data}, upsert=True)

      await ctx.respond("""Поздравляем вы зарегестрированы""")


@bot.command()
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
    await ctx.respond('<@&1167993718704447519>.', embed=embed, view=view)
  else:
    await ctx.respond(
        """Вы не зарегестрированы.\nДля регестрации воспользуйтесь коммандой /reg"""
    )


@bot.command()
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
    await ctx.respond('<@&1167993718704447519>.', embed=embed, view=view)
  else:
    await ctx.respond(
        """Вы не зарегестрированы.\nДля регестрации воспользуйтесь коммандой /reg"""
    )


@bot.command(
    description=
    """Вызов на дуэль. В пункте player:@jarjar пинганите человека чере @""")
async def v1(ctx, member: discord.Member):
  db = client.get_database('Rating_data_base')
  collection = db['Collection_data']

  check_author = collection.find_one({"_id": str(ctx.author.id)})
  user_document = collection.find_one({"_id": str(member.id)})

  if check_author:
    if member.id == 1150018596307734579:
      await ctx.respond('Я не думаю что ты способен победить меня xd')
    # Запускаем класс с кнопками если все прекрастно
    elif ctx.author.id == member.id:
      await ctx.respond('Вы не можете вызвать самого себя')
    else:
      if user_document:
        guild = bot.get_guild(guild_id)
        view = button1v1View(ctx, member.id, db, guild)
        await ctx.respond(
            f'Вызов на столкновение игрока <@{member.id}> (`{user_document["Rating_1v1"]}`)',
            view=view)

      else:
        await ctx.respond('Этот игрок не зарегестрирован.')
  else:
    await ctx.respond(
        """Вы не зарегестрированы.\nДля регестрации воспользуйтесь коммандой /reg"""
    )


# @bot.command()
# @commands.has_permissions(administrator=True)

bot.run(token)
