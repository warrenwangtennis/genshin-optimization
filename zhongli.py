from util import *

base_hp = 14695
base_atk = 251

base_stats = Stats({
	'hpf': 4780,
	'atkf': 311,
	'crit': 5 * 2 + 50,
	'dmgp': 28.8 + 15 + 20
})

# main_stats = Stats({
# 	'hpf': 4780,
# 	'atkf': 311,
# 	'hpp': 46.6,
# 	'dmgp': 46.6 + 15 + 20,
# 	'crit': 62.2
# })

# num_subs = {
# 	'hpp': 5,
# 	'atkp': 5,
# 	'crit': 22
# }

# sub_stats = Stats({x: num_subs[x] * sub_vals[x] for x in num_subs})

class Char(Base_Char):
	def __init__(self, x):
		if type(x) is Char:
			self.weapon = x.weapon
			self.base_stats = Stats(x.base_stats)
			self.base_hp = x.base_hp
			self.base_atk = x.base_atk
			self.mains = x.mains
			self.subs = {**x.subs}
		else:
			self.weapon = x
			self.base_stats = empty_stats + base_stats + self.weapon['stats']
			self.base_hp = base_hp
			self.base_atk = base_atk + self.weapon['base_atk']
			self.mains = ()
			self.subs = defaultdict(int)

	def get_hp(self, stats):
		return self.base_hp * (1 + stats.d['hpp']/100) + stats.d['hpf']

	def get_atk(self, stats):
		hp = self.get_hp(stats)
		atk = self.base_atk * (1 + stats.d['atkp']/100) + stats.d['atkf']
		if self.weapon['homa'] == 1:
			atk += 1.8/100 * hp
		elif self.weapon['homa'] == 2:
			atk += 3.4/100 * hp
		return atk

	def score(self):
		stats = self.get_stats()
		hp = self.get_hp(stats)
		atk = self.get_atk(stats)
		if stats.d['crit'] > 400:
			cr = 100
			cd = stats.d['crit'] - 200
		else:
			cr = stats.d['crit'] / 4
			cd = stats.d['crit'] / 2
		crit = 1 + cr/100 * cd/100
		dmgp = 1 + stats.d['dmgp']/100
		return (atk * 834.68/100 + hp * 33/100) * crit * dmgp

weapons = [deathmatch(1, False), homa1(), homa5(), lithic_spear(1, 4), lithic_spear(5, 4)]
chars = [Char(x) for x in weapons]
for c in chars:
	c.optimize(30)
base_score = chars[0].score()

for i, c in enumerate(chars):
	score = c.score()
	print(weapons[i]['name'], score, (score - base_score)/base_score*100)
	print(c.mains)
	print(dict(c.subs))