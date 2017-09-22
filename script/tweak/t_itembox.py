#!/usr/bin/env python
# -*- coding: utf-8 -*-
ID = 12001005 #東可動橋 南側のアイテムBOX

NORMAL_HAIR_MALE = (
	("ナチュラル", 0),
	("ロング", 1),
	("ワイルド", 2),
	("ワンレングス", 3),
	("クールカット", 4),
	("ボーイズ", 5),
	("オールバック", 6),
	("スキンヘッド", 7),
	("コンサバティブ", 8),
)

NORMAL_HAIR_FEMALE = (
	("ショート", 0),
	("レイヤー", 1),
	("ロング", 2),
	("外巻きヘア", 3),
	("内巻きヘア", 4),
	("セミロング", 7),
	("ナチュラル", 8),
	("アンティーク", 9),
	("ベリーショート", 14),
)

REFINE_HAIR_MALE = (
	("リファインナチュラル", 200),
	("リファインボーイズ", 201),
	("リファインコンサバティブ", 202),
	("リファインワンレングス", 203),
	("リファインワイルド", 204),
	("リファインオールバック", 205),
	("リファインロング", 206),
	("リファインクールカット", 207),
)

REFINE_HAIR_FEMALE = (
	("リファインナチュラル", 200),
	("リファインアンティーク", 201),
	("リファインレイヤー", 202),
	("リファインショート", 203),
	("リファイン外巻きヘア", 204),
	("リファイン内巻きヘア", 205),
	("リファインセミロング", 206),
	("リファインロング", 207),
	("リファインベリーショート", 208),
)

from lib import script
def main(pc):
	selects = (
		"dyeing",
		"normal hair",
		"refine hair",
		"hair salon",
		"hair ex change",
		"hair catalog",
		"reincarnation_ex",
		"cancel",
	)
	result = script.select(pc, selects , "select")
	if result == 1:
		script.dyeing(pc)
	elif result == 2:
		if pc.gender == 0:
			use_hair_list(pc, "どの髪型にする？", NORMAL_HAIR_MALE)
		else:
			use_hair_list(pc, "どの髪型にする？", NORMAL_HAIR_FEMALE)
	elif result == 3:
		if pc.gender == 0:
			use_hair_list(pc, "どの髪型にする？", REFINE_HAIR_MALE)
		else:
			use_hair_list(pc, "どの髪型にする？", REFINE_HAIR_FEMALE)
	elif result == 4:
		script.show_haircat(pc, 0)
	elif result == 5:
		script.show_haircat(pc, 1)
	elif result == 6:
		script.show_haircat(pc, 2)
	elif result == 7:
		script.reincarnation_ex(pc)

def use_hair_list(pc, title, hair_list):
	index = script.select(pc, tuple(i[0] for i in hair_list)+("cancel", ), title)
	if index == len(hair_list) + 1:
		return
	with pc.lock:
		pc.hair = hair_list[index - 1][1]
		pc.wig = -1
	script.update_head(pc)
