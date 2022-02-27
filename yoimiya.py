from util import *

base_hp = 10164
base_atk = 323

base_stats = Stats({
	'hpf': 4780,
	'atkf': 311,
	'atkp': 18,
	'cr': 5 + 19.2,
	'cd': 50,
	'dmgp': 2*10*0.75 + 50
})

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
		return atk

	def score(self, dbg=False):
		stats = self.get_stats()
		hp = self.get_hp(stats)
		atk = self.get_atk(stats)
		critm, cr, cd = get_optimal_critm(stats.d['cr']*2 + stats.d['cd'])
		dmgm = 1 + stats.d['dmgp']/100
		if dbg:
			print(hp, atk, cr, cd, stats.d['em'], dmgm)
		return atk * critm * dmgm

	def copy(self):
		return Char(self)

weapons = [rust(5), thundering_pulse(1), thundering_pulse(5)]
chars = [Char(x) for x in weapons]
for c in chars:
	c.optimize(30, 30)
base_score = chars[0].score()

for i, c in enumerate(chars):
	score = c.score(False)
	print(weapons[i]['name'], (score - base_score)/base_score*100)
	# print(c.mains)
	# print(dict(c.subs))
	# print()