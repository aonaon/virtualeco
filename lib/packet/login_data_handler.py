#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
import hashlib
import os
from lib import env
from lib import general
from lib.packet import packet
from lib import users
from lib.packet.packet_struct import *
DATA_TYPE_NOT_PRINT = (
	"000a", #接続確認
)

class LoginDataHandler:
	def __init__(self):
		self.user = None
		self.pc = None
		self.word_front = pack_unsigned_int(
			general.randint(0, general.RANGE_INT[1])
		)
		self.word_back = pack_unsigned_int(
			general.randint(0, general.RANGE_INT[1])
		)
	
	def send(self, *args):
		self.send_packet(general.encode(packet.make(*args), self.rijndael_obj))
	
	def stop(self):
		if self.user:
			self.user.reset_login()
			self.user = None
		self._stop()
	
	def handle_data(self, data_decode):
		#000a 0001 000003f91e07e221
		data_decode_io = general.stringio(data_decode)
		while True:
			data = io_unpack_short_raw(data_decode_io)
			if not data:
				break
			data_io = general.stringio(data)
			data_type = data_io.read(2).encode("hex")
			if data_type not in DATA_TYPE_NOT_PRINT:
				general.log("[login]",
					data[:2].encode("hex"), data[2:].encode("hex"))
			handler = self.name_map.get(data_type)
			if not handler:
				general.log_error("[login] unknow packet type",
					data[:2].encode("hex"), data[2:].encode("hex"))
				return
			try:
				handler(self, data_io)
			except:
				general.log_error("[login] handle_data error:", data.encode("hex"))
				general.log_error(traceback.format_exc())
	
	def do_0001(self, data_io):
		#接続・接続確認
		data = data_io.read()
		general.log("[login] eco version", unpack_unsigned_int(data[:4]))
		self.send("0002", data) #認証接続確認(s0001)の応答
		self.send("001e", self.word_front+self.word_back) #PASS鍵
		general.log("[login] send word",
			self.word_front.encode("hex"), self.word_back.encode("hex"),
		)
	
	def do_001f(self, data_io):
		#認証情報
		username = io_unpack_str(data_io)
		password_sha1 = io_unpack_raw(data_io)[:40]
		general.log("[login]", "login", username, password_sha1)
		for user in users.get_user_list():
			with user.lock:
				if user.name != username:
					continue
				user_password_sha1 = hashlib.sha1(
					"".join((str(unpack_unsigned_int(self.word_front)),
							user.password,
							str(unpack_unsigned_int(self.word_back)),
							))).hexdigest()
				if user_password_sha1 != password_sha1:
					self.send("0020", user, "loginfaild") #アカウント認証結果
					return
				if user.login_client:
					user.reset_login()
					self.send("0020", user, "isonline") #アカウント認証結果
					return
				user.reset_login()
				user.login_client = self
				self.user = user
				self.send("0020", user, "loginsucess") #アカウント認証結果
				###Delete Ver358 Login
				break
		else:
			self.send("0020", user, "loginfaild") #アカウント認証結果

	def do_002f(self, data_io):
		self.send("0030")

	def do_000a(self, data_io):
		#接続確認
		self.send("000b", data_io.read()) #接続・接続確認(s000a)の応答
	
	def do_0031(self, data_io):
		#接続確認
		general.log("[login] requested server information")
		self.send("0032")#接続先通知要求(0031)の応答
		self.send("0033", "login")#接続先情報送信(ワールドログインサーバーAddr)
		#TODO: temp ws2_32 reconnect fix
		self.send("0033", "login")#接続先情報送信(ワールドログインサーバーAddr)
		self.send("0034")#接続先通知終了(0031)の応答


LoginDataHandler.name_map = general.get_name_map(LoginDataHandler.__dict__, "do_")