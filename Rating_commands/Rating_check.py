import discord
import pymongo
import json


class Rating_Role():
  def __init__(self, ctx, collection, Dictionaries_Team,guild):
    self.ctx = ctx
    self.collection = collection
    self.Dictionaries_Team = Dictionaries_Team
    self.guild = guild
    self.roleup(ctx, collection, Dictionaries_Team, guild)

  def spisok(self, collection, id):
    check_author = collection.find_one({"_id": str(id)})
    sl=[check_author['Rating_1v1'],check_author['Rating_2v2'],check_author['Rating_4v4']]

    for i in range(2):
      for j in range(3-i-1):
        if sl[j]<sl[j+1]:
          sl[j], sl[j+1] = sl[j+1], sl[j]
    return sl


  def levelR(self, r, l):
    if r > 1200:
      r -= 400
      l += 1
      return self.levelR(r, l)
    else:
      return 


  def check_level(self, Roles, role, member, guild, level):
    if role.id in Roles['VIP']:
      return 'V'
    elif role in Roles['L']:
      if level == Roles['L'].index(role.id):
        return 'L-0'
      else:
        member.remove_roles(role)
        member.add_roles(guild.get_role(Roles['L'][level]))
        return 'L-1'
    elif role.id in Roles['D']:
      if level == Roles['D'].index(role.id):
        return 'D-0'
      else:
        member.remove_roles(role)
        member.add_roles(guild.get_role(Roles['D'][level]))
        return 'D-1'
    elif role.id in Roles['M']:
      return 'M'
    else:
      print('Error roles')

  def roleup(self,ctx, collection, DT, guild):
    self.collection = collection
    level = 0
    Roles = json.load(open('Role.json'))
    for i, j in DT.items():
      ii = DT[i]['id']
      member = guild.get_member(DT[i]['id'])
      levels = self.spisok(self.collection, ii)
      level = self.levelR(levels[1], 1)
      roles = member.roles
      role = roles[1]
      self.check_level(Roles, role, member, guild, level)