import os
import json
import discord
import pymongo


class check_name_and_reg():

  print('check_name_and_reg работает!')
  # if hourse <= 50:
  #   rating = 200
  # elif hourse <= 300:
  #   rating = 400
  # elif hourse <= 4000:
  #   rating = 600
  # else:
  #   rating = 1000
  
  # db = client.get_database('Rating_data_base')
  # listdb_users = db.Rating_data_base.find({})
  # list_db_users = list(listdb_users)
  # idUsers = list_db_users[0]
  
  # # предполагаем что `db` это ваша база данных MongoDB
  # # и `user_id` это id пользователя (ctx.author.id)
  # user_id = str(ctx.author.id)  # преобразуем в строку, поскольку в JSON ключи являются строками
  
  # # Создаем запрос в MongoDB для поиска пользователя по id.
  # user_document = db.Rating_data_base.find_one({"_id": user_id})
  
  
  # # Проверяем найден ли id пользователя в базе данных
  # if user_document:
  #   Data = idUsers[str(ctx.author.id)]
  #   EAName = Data['EA_Name']
  #   await ctx.respond(f'Вы уже зарегестрированы под никнемом {EAName}.')
  
  
  # else: 
  #   async def check_name_in_database(db, name):
  #     user_document = db.Rating_data_base.find_one({"EA_Name": name})
  #     if user_document:
  #       await ctx.respond(
  #         f"""Имя {name} уже занято пользователем.\n
  #         Обратитесь пожалуйста в Администрацию.""")
  #       return ()
  #       return True
  #     else:
  #       idUsers[str(ctx.author.id)] = {
  #         'EA_Name': name,
  #         'Rating_1v1': rating,
  #         'Rating_2v2': rating,
  #         'Rating_4v4': rating
  #       }
  
  #       db.Rating_data_base.update_one({}, {"$set":idUsers})
        
  #       await ctx.respond(
  #         f"""Поздравляем вы зарегестрированы\nВаши ваши данные:
  #       {idUsers[str(ctx.author.id)]}""")
  #       return False