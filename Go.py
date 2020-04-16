import discord
from discord import utils

import config

class MyClient(discord.Client):
	async def on_ready(self):
		print('Бот подключился - {0}!'.format(self.user))

	async def on_raw_reaction_add(self, payload):
		if payload.message_id == config.POST_ID:
			channel = self.get_channel(payload.channel_id) # получаем объект канала
			message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
			member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию

			try:
				emoji = str(payload.emoji) # эмоджик который выбрал юзер
				role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # объект выбранной роли (если есть)
			
				if(len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
					await member.add_roles(role)
					print('[Удача] Пользователь {0.display_name} получил роль {1.name}'.format(member, role))
				else:
					await message.remove_reaction(payload.emoji, member)
					print('[ОШИБКА] Слишком много ролей для пользователя {0.display_name}'.format(member))
			
			except KeyError as e:
				print('[ОШИБКА] Роль не найдена ' + emoji)
			except Exception as e:
				print(repr(e))

	async def on_raw_reaction_remove(self, payload):
		channel = self.get_channel(payload.channel_id) # получаем объект канала
		message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
		member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию

		try:
			emoji = str(payload.emoji) # эмоджик который выбрал юзер
			role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # объект выбранной роли (если есть)

			await member.remove_roles(role)
			print('[Удачно] Роль {1.name} была удалена {0.display_name}'.format(member, role))

		except KeyError as e:
			print('[ОШИБКА] Роль не найдена ' + emoji)
		except Exception as e:
			print(repr(e))

# RUN
client = MyClient()
client.run(config.TOKEN)