from util import *

base_hp = 12858
base_atk = 342

base_stats = Stats({
	'hpf': 4780,
	'atkf': 311,
	'atkp': 20,
	'cr': 5 + 40 + 15,
	'cd': 50 + 38.4,
	'dmgp': 18 + 15 + 34.6,
	'nap': 15, # half effectiveness of 6s boost after E
	'cap': 15, # half effectiveness of 6s boost after E
})

na_mist_stacks = [0] + [3] * 3 * 4
ca_mist_stacks = [3] * 3
e_mist_stacks = [1, 3]
q_mist_stacks = [3]


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
		if 'jade_cutter' in self.weapon:
			atk += refine_val(1.2, 2.4, self.weapon['jade_cutter'])/100 * hp
		return atk

	def score(self, dbg=False):
		stats = self.get_stats()
		hp = self.get_hp(stats)
		atk = self.get_atk(stats)
		critm, cr, cd = get_optimal_critm(stats.d['cr']*2 + stats.d['cd'])
		dmgp = stats.d['dmgp']
		nap = stats.d['nap']
		cap = stats.d['cap']

		tot = 0
		for mist_stacks in na_mist_stacks:
			mistp = from_mist(mist_stacks, self.weapon)
			dmgm = 1 + (dmgp + mistp + nap)/100
			tot += (90.39)/100*(atk * critm * dmgm)
		for mist_stacks in ca_mist_stacks:
			mistp = from_mist(mist_stacks, self.weapon)
			dmgm = 1 + (dmgp + mistp + cap)/100
			tot += (108.97*3)/100*(atk * critm * dmgm)
		for mist_stacks in e_mist_stacks:
			mistp = from_mist(mist_stacks, self.weapon)
			dmgm = 1 + (dmgp + mistp)/100
			tot += (430.56)/100*(atk * critm * dmgm)
		for mist_stacks in q_mist_stacks:
			mistp = from_mist(mist_stacks, self.weapon)
			dmgm = 1 + (dmgp + mistp)/100
			tot += (15*202.14+303.21)/100*(atk * critm * dmgm)
			
		if dbg:
			print('hp={:.0f} atk={:.0f} cr={:.0f} cd={:.0f}'.format(hp, atk, cr, cd))
		return tot

	def real_dmg(self):
		score = self.score()
		return score * 1.15 * (100+90)/(200+90+100)

weapons = [black_sword(1), black_sword(5), jade_cutter(1), jade_cutter(5), aquila(1), aquila(5), summit(1, 4.5, 1), summit(5, 4.5, 1), mistsplitter(1), mistsplitter(5)]
# weapons = [black_sword(1), black_sword(5), mistsplitter(1), mistsplitter(5)]
chars = [Char(x) for x in weapons]
for c in chars:
	c.optimize(30, 30)
base_score = chars[0].score()

for i, c in enumerate(chars):
	score = c.score(True)
	print(weapons[i]['name'], '{:.2f}'.format((score - base_score)/base_score*100))
	print(c.mains)
	print(dict(c.subs))
	print()