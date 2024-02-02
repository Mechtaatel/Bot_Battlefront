import logging
import os
import json

import discord
from discord.ext import commands
from discord.ui import Button, View, Select

import requests
import time
from background import keep_alive #импорт функции для поддержки работоспособности


from Rating_commands.v1 import button1v1View
from Rating_commands.v2 import button2v2View
from Rating_commands.Rating_Role import Rating_Role_View
#from Rating_commands.reg import check_name_and_reg



import pymongo
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient



intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = discord.Bot()

version_bot = 1.1.1
  

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





#Создайте экземпляр команды с косой чертой
logging.basicConfig(level=logging.INFO)


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
  user_document = collection.find_one({"_id":user_id})

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
      
      new_data = {
      'EA_Name': name,
      'Rating_1v1': rating,
      'Rating_2v2': rating,
      'Rating_4v4': rating
      }
      
      collection.update_one({'_id': user_id},{"$set":new_data}, upsert=True)
         
      await ctx.respond(
           """Поздравляем вы зарегестрированы""")





      
    
@bot.command()
async def v2(ctx):
  check_author = collection.find_one({"_id": str(ctx.author.id)})
  if check_author:
    Author = collection.find_one({"_id": str(ctx.author.id)})
    embed = discord.Embed(title=
                          '',
       description=f'Игрок <@{ctx.author.id}> начинает поиск игроков в режим 2 на 2',
      color=0x1c2951)
    embed.add_field(name="",
                    value="",
                    inline=False)
    embed.add_field(name=f"`{Author['Rating_2v2']}`",
                    value=f"`{Author['EA_Name']}`\n`___`",
                    inline=True)
    embed.add_field(name="`0`",
                    value=f"`___`\n`___`",
                    inline=True)
    embed.set_footer(text="")
    view=button2v2View(ctx,collection,Author)
    await ctx.respond('<@&1167993718704447519>.',embed=embed,view=view)
  else:
    await ctx.respond(
      """Вы не зарегестрированы.\nДля регестрации воспользуйтесь коммандой /reg""")

    
  










@bot.command(description="""Вызов на дуэль. В пункте player:@jarjar пинганите человека чере @""")
async def v1(ctx, player: str):
  # Ниже избовляемся от ковычек и собачки в сообщение
  liist = ['<', '>', '@']
  for i in liist:
    player = player.replace(i, '')

  db = client.get_database('Rating_data_base')
  collection = db['Collection_data']

  check_author = collection.find_one({"_id": str(ctx.author.id)})
  user_document = collection.find_one({"_id":player})
  
  if check_author:
    if player == '1150018596307734579':
      await ctx.respond('Я не думаю что ты способен победить меня xd')
    # Запускаем класс с кнопками если все прекрастно
    elif ctx.author.id == int(player):
      await ctx.respond('Вы не можете вызвать самого себя')
    else:
      if user_document:
          view = button1v1View(ctx, player,db)
          await ctx.respond(
            f'Вызов на столкновение игрока <@{player}> (`{user_document["Rating_1v1"]}`)',
            view=view)
          
      else:
        await ctx.respond('Этот игрок не зарегестрирован.')
  else:
    await ctx.respond(
      """Вы не зарегестрированы.\nДля регестрации воспользуйтесь коммандой /reg""")











@bot.command()
@commands.has_permissions(administrator=True)
async def level_join(ctx):

  embed = discord.Embed(title='Создание рейтинговых ролей.',
                         description='description opcioanl',
                        color=0x00ff00)
  embed.add_field(name="Поле 1", value="Значение поля 1", inline=False)
  embed.add_field(name="Поле 2", value="Значение поля 2", inline=True)
  embed.add_field(name="Поле 3", value="Значение поля 3", inline=True)
  embed.set_footer(text="Текст в футере")
  # embed.set_image(url="URL_изображения")
  # embed.set_thumbnail(url="URL_миниатюры")
  # embed.set_author(name="Автор", url="URL_автора", icon_url="URL_иконки_автора")
  view = Rating_Role_View(ctx)
  await ctx.send(embed=embed, view=view)









keep_alive()
bot.run(os.environ['token'])
