#!/usr/bin/env python
# -*- coding: utf-8 -*-

ID = (1000050001, "partner_motion_together")

COMBI_MOTIONS = {
	10158800: ((85, 2, 9000, 1, 2048),	(85, 1, 9001, 1, 158),	(85, 1, 9002, 1, 9002), ),	#ブリキングＲＸ１・アルマ
	10159200: ((85, 0, 9003, 0, 9003),	(85, 0, 9004, 0, 9003),	(85, 0, 9005, 0, 9005), ),	#クイーンビー・アルマ
	10159700: ((85, 0, 9006, 0, 9006),	(85, 0, 9007, 0, 9007),	(85, 0, 9008, 0, 9008),	),	#アルカナハート・アルマ
	10159800: ((85, 0, 9009, 0, 9009),	(85, 0, 9010, 0, 9010),	(85, 0, 9011, 0, 9011),	),	#ウィスプ・アルマ
	10160200: ((85, 0, 9012, 0, 9012),	(85, 0, 9013, 0, 9013),	(85, 0, 9014, 0, 9014),	),	#スケルトンシューター・アルマ
	10160800: ((85, 0, 9015, 0, 9015),	), #スペクター・アルマ
	10164200: ((85, 0, 9016, 0, 9016),	), #ニドエッグ・アルマ
	10165100: ((85, 0, 9017, 0, 9017),	), #ホウオウ・アルマ
	10165500: ((85, 0, 9018, 0, 9018),	), #ニドエッグ・アルマ
	10166300: ((85, 0, 9019, 0, 9019),	), #ベイヤール・アルマ
	10166900: ((85, 0, 9020, 0, 9020),	), #サンドラット・アルマ
	10167700: ((85, 0, 9021, 0, 9021),	), #クリスタル・アルマの設定,
	10168300: ((85, 0, 9022, 0, 9022),	), #ホワイトファング・アルマの設定,
	10168600: ((85, 0, 9037, 0, 9037),	(85, 0, 9038, 0, 9038),	), #シナモン・アルマの設定,
	10169400: ((85, 0, 9039, 0, 9039),	), #サイクロプス・アルマの設定
	10170400: ((85, 0, 9040, 0, 9040),	), #クリムゾンバウ・アルマの設定
	10170700: ((85, 1, 9041, 1, 9041),	), #バルーンピッグー・アルマの設定
}

def pmt_use(pc, motion_id):
	if not pc.pet:
		return
	with pc.lock and pc.pet.lock:
		pet_item = pc.item.get(pc.equip.pet)
		if pet_item.item_id in COMBI_MOTIONS:
			motion_list = COMBI_MOTIONS[pet_item.item_id]
		else:
			motion_list = ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0),)
		motion_temp = motion_list[motion_id]
		if motion_temp[0] == 85:
			dir_temp = pc.dir
			if dir_temp >= 0 and dir_temp < 2:
				dir_temp = 0
			elif dir_temp > 1 and dir_temp < 4:
				dir_temp = 2
			elif dir_temp > 3 and dir_temp < 6:
				dir_temp = 4
			elif dir_temp > 5 and dir_temp < 8:
				dir_temp = 6
			pet_pos = dir_temp
			pet_dir = motion_temp[1] + dir_temp
			pc_dir = motion_temp[3] + dir_temp
			if pet_pos > 7:
				pet_pos -= 7
			if pet_dir > 7:
				pet_dir -= 7
			if pc_dir > 7:
				pc_dir -= 7
			motion_set = (pet_pos, pet_dir, motion_temp[2], pc_dir, motion_temp[4])
		else:
			motion_set = motion_temp
		result = motion_set
	return result
def main(pc):
	return