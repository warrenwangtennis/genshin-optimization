from util import *

base_hp = 13103
base_atk = 323

base_stats = Stats({
	'crit': 5 * 2 + 50 + 38.4 + 15 * 2,
})

main_stats = Stats({
	'hpf': 4780,
	'atkf': 311,
	'atkp': 46.6 + 18,
	'dmgp': 46.6 + 15,
	'crit': 62.2
})

num_subs = {
	'atkp': 7,
	'crit': 22
}

sub_stats = Stats({x: num_subs[x] * sub_vals[x] for x in num_subs})

class Char:
	def __init__(self, weapon):
		self.weapon = weapon
		self.stats = empty_stats + base_stats + main_stats + sub_stats + weapon['stats']
		self.base_hp = base_hp
		self.base_atk = base_atk + weapon['base_atk']

	def get_hp(self):
		return self.base_hp * (1 + self.stats.d['hpp']/100) + self.stats.d['hpf']

	def get_atk(self):
		hp = self.get_hp()
		atk = self.base_atk * (1 + self.stats.d['atkp']/100) + self.stats.d['atkf']
		if 'jade' in self.weapon:
			atk += refine_val(1.2, 2.4, self.weapon['jade'])/100 * hp
		return atk

	def score(self):
		hp = self.get_hp()
		atk = self.get_atk()
		cr = self.stats.d['crit'] / 4
		cd = self.stats.d['crit'] / 2
		crit = 1 + cr/100 * cd/100
		dmgp = 1 + self.stats.d['dmgp']/100
		print(hp, atk, cr, cd, dmgp)
		return atk * crit * dmgp

weapons = [make_black_sword(1, 0.9), make_jade_cutter(1), make_jade_cutter(5), make_aquila(1), make_aquila(5)]
chars = [Char(x) for x in weapons]
scores = [c.score() for c in chars]

for i, score in enumerate(scores):
	print(weapons[i]['name'], score, (score - scores[0])/scores[0]*100)