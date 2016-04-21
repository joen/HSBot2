class Telegram():
	FOLLOWER = ()
	NAME = "telegram"

	def __init__(self):
		updater = Updater(token=c.TOKEN)
		dispatcher = updater.dispatcher
		f = open(c.TFILE, 'r')
		self.FOLLOWER = f.read().split(",")
		f.close()
		if "" in self.FOLLOWER:
			while "" in self.FOLLOWER:
				self.FOLLOWER.remove("")
			f = open(c.TFILE, 'w')
			f.write(",".join(self.FOLLOWER))
			f.close()

		dispatcher.addTelegramCommandHandler('delete', self.deleteme)
		dispatcher.addTelegramCommandHandler('add', self.addme)
		dispatcher.addTelegramMessageHandler(self.echo)
		dispatcher.addUnknownTelegramCommandHandler(self.notunderstand)

		start_new_thread(updater.start_polling,(5,))

	def echo(self,bot, update):
		#print(update)
		sID = str(update.message.chat.id)
		sName = update.message.chat.first_name
		sText = update.message.text
		#TODO hier fehlt irgendwie die sender var
		print(sID)
		print(sName)
		print(sText)
		self.sendPublic(sName+": "+sText,bot,sID)
		self.toController(sText,sName)

	def deleteme(self,bot,update):
		#print("d")
		user = str(update.message.chat_id)
		#print("user: "+user)
		#print("follower: "+str(self.FOLLOWER))
		if user in self.FOLLOWER:
			#print("ja")
			while user in self.FOLLOWER:
				self.FOLLOWER.remove(user)
				print("entferne")
			f = open(c.TFILE, 'w')
			f.write(",".join(self.FOLLOWER))
			f.close()
			#print("follower: "+str(self.FOLLOWER))
			self.sendPrivat(update.message.chat_id,"Bis Bald ...",bot)
		else:
			self.sendPrivat(update.message.chat_id,"Du bist nicht in meiner Liste.",bot)

	def addme(self,bot,update):
		#print("a")
		user = str(update.message.chat_id)
		if user in self.FOLLOWER:
			self.sendPrivat(update.message.chat_id,"Du bist schon in meiner Liste.",bot)
			
		else:
			f = open(c.TFILE, 'a')
			if len(self.FOLLOWER) == 0:
				f.write(str(user))
			else:
				f.write(","+str(user))                  
			f.close()
			self.FOLLOWER.append(user)
			#print("follower: "+str(self.FOLLOWER))
			self.sendPrivat(update.message.chat_id,"Du wurdest hinzugefügt.",bot)

	def notunderstand(self,bot,update):
		bot.sendMessage(chat_id=update.message.chat_id, text="/add : dich anmelden\n/delete : dich abmelden")

	def sendPublic(self,sendtext,bot=False,sender=0):
		#print("3")
		if not bot:
			#print("6")
			bot = Bot(token=c.TOKEN)
		#print("7")
			
		if sender == 0 or sender in self.FOLLOWER:
			#print("4")
			for i in self.FOLLOWER:
				if i != sender:
					#print("1")
					bot.sendMessage(chat_id=i, text=sendtext)
		else:
			#print("5")
			self.sendPrivat(sender,"Du bist nicht teil der Gruppe: tippe /add um beizutreten",bot)

	def sendPrivat(self,reciever,sendtext,bot=False):
		if not bot:
			bot = Bot(token=c.TOKEN)
		#print("Privat: "+sendtext)
		bot.sendMessage(chat_id=reciever, text=sendtext)

	def heartbeat(self):
		return True
	
	def sendTo(self,nick,uid,text):
		if nick == c.JNICK:
			txt = text
		else:
			txt = nick +": "+ text
			
		self.sendPublic(txt)
		
	def toController(self,text,nick):
		HOST = '127.0.0.1'
		PORT = c.CMSGPORT
		
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((HOST, PORT))
			data = {'service':self.NAME,'text':str(text),'nick':str(nick)}
			s.sendall(json.dumps(data))
			data = s.recv(1024)
			s.close()
			return data
		except Exception as e:
			print("ERROR")
			print(e)
			print(sys.exc_info()[0])	
			return False
