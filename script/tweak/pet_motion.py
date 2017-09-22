#-*- coding: utf-8 -*-
from lib import script
from lib import general
ID = (1000000000, "pet_motion") #仮 skill.2442 信頼の証

motion_ride = (
	#select(selection , motion)
	("歩く", 121),
	("走る", 122),
	("攻撃！", 341),
	("痛っ！", 361),
	("倒れる", 362),
	("ぐったり", 363),
	("アピール", 210),
	("元に戻す", 111),
)

motion_head = (
	#基本モーション
	("歩く", 121),
	("走る", 122),
	("攻撃！", 341),
	("痛っ！", 361),
	("倒れる", 362),
	("ぐったり", 363),
	("アピール", 364),
)

motion_foot = (
	#基本モーション
	("元に戻す", 111),
)

motion_common = motion_head + (
	#
	("＃400", 400),
	("＃555", 555),
	("＃556", 556),
	("＃557", 557),
	("＃558", 558),
	("＃559", 559),
	("手を振る", 113),
	("座る", 135),
) + motion_foot

m_template = motion_head + (
	#
	("＃400", 400),
	("＃555", 555),
	("＃556", 556),
	("＃557", 557),
	("＃558", 558),
	("＃559", 559),
	("手を振る", 113),
	("座る", 135),
) + motion_foot

m_tinyzero_alma = motion_head + (
	#タイニーアルマ系
	("ダンス", 400),
	("考える", 555),
	("君に憑依っ☆", 556),
	("動揺する", 557),
	("み～つけた！", 558),
	("決めポーズ", 559),
	("手を振る", 113),
	("座る", 135),
) + motion_foot

lean = motion_head + (
	#リーン
	("メンテナンス", 555),
	("ビットに座る", 556),
	("手を振る", 113),
	("座る", 135),
) + motion_foot



PET_ID_LIST = {
		#タイニー関連: #N/A,#
		20250000:  m_tinyzero_alma,#タイニーゼロ
		17460000:  m_tinyzero_alma,#タイニーゼロ・アルマ
		17460001:  m_tinyzero_alma,#タイニーゼロ・アルマ＋
		17790000:  m_tinyzero_alma,#タイニーゼロ（Mary）
		#ドミニオン世界拡張: #N/A,#
		17580000:  lean,#リーン
}



def main(pc):
	if not pc.pet:
		return
	with pc.lock and pc.pet.lock:
		pet_item = pc.item.get(pc.equip.pet)
		if not pet_item.pet_id in PET_ID_LIST:
			if pc.item.get(pc.equip.pet).check_type(general.RIDE_TYPE_LIST):
				motion_list = motion_ride
			else:
				motion_list = motion_common
		else:
			motion_list = PET_ID_LIST[pet_item.pet_id]
		result = script.select(pc, tuple(i[0] for i in motion_list), "どれにする")
		motion = motion_list[result - 1][1]
		if pc.item.get(pc.equip.pet).check_type(general.RIDE_TYPE_LIST):
			script.motion_loop(pc, motion)
		else:
			script.petmotion_loop(pc, motion)