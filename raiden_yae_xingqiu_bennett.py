from core import *
from char_bps import *
from collections import defaultdict
import global_

class RaidenYaeXingqiuBennett(Team):
	def __init__(self, chars):
		super().__init__(chars)

	def score(self, dbg=False):
		raiden, yae, xingqiu, bennett = self.chars
		all_stats = self.get_stats()
		raiden_stats, yae_stats, xingqiu_stats, bennett_stats = all_stats
		# assume buffs cannot buff buffs

        # artifact bonuses
		raiden_stats.d['er'] += 20 # other effect hardcoded into q dmg
		yae_stats.d['atkp'] += 18 + 18
		xingqiu_stats.d['dmgp'] += 15
		xingqiu_stats.d['qp'] += 20
		bennett_stats.d['qp'] += 20

		# raiden er requirement reduction
		for s in all_stats:
			s.d['energyf'] += 2.5 * 5 * (1 + ((raiden_stats.d['er'] - 100) * 0.6)/100)

		# bennett favonius sword
		if 'favonius_sword' in bennett.weapon:
			for s in all_stats:
			    s.d['energyf'] += 4 * s.d['er']/100 * 2 # 2 procs, assume r5, approx

		# no further ER buffs, disqualify not enough ER
		er_deficit = sum(max(c.er_req * (1 - s.d['energyf']/c.q_cost) - s.d['er'], 0) for c, s in zip(self.chars, all_stats))
		if er_deficit > 0:
			return -er_deficit


		# Raiden E -> XQ E + Q + E + n1 -> Yae 3E + n1 + Q + 3E + n1 -> Bennett Q + n1 + E + n1 -> Raiden Q + 3xn5
		# 22s, assume have excess time
		
		tot = 0

		global_.dbg = dbg
		global_.dmg_log = [] if dbg else None

		# Raiden E

		tot += raiden.dmg_e(raiden_stats, 10, 10, ticks=12, in_q=False)

		# START Raiden E buff - lasts forever
		for c, s in zip(self.chars, all_stats):
			s.d['qp'] += c.q_cost * 0.3

		# Xingqiu XQ E + Q + E + n1

		tot += xingqiu.dmg_e(xingqiu_stats, 10, False)
		tot += xingqiu.dmg_q(xingqiu_stats, -2.5, ticks=15)

		if 'sac_sword' in xingqiu.weapon:
			r = xingqiu.weapon['sac_sword']
			if r < 4:
				print('sac_sword refinement ' + r + ' not supported')
				exit()
			tot += xingqiu.dmg_e(xingqiu_stats, 10, True) # q hasn't hit

		# Yae 3E + n1 + Q + 3E + n1

		tot += yae.dmg_e(yae_stats, 10, 19/3, 3)
		tot += yae.dmg_q(yae_stats, 10, 3)

		# Bennett Q + n1 + E + n1

		# START Bennett Q atk buff and 4NO buff, last forever
		# only affect on field, check !!!
		for s in all_stats:
			s.d['atkf'] += bennett.q_atkf_buff(bennett_stats)
			s.d['atkp'] += 20

		# Raiden E continued
		tot += raiden.dmg_e(raiden_stats, 10, 10, ticks=10, in_q=True)

		# Raiden Q + (N5)x3
		tot += raiden.dmg_q(raiden_stats, 10, 3)

		if dbg:
			global_.dmg_log.append(("total", tot))
			for dmg_type, dmg_val in global_.dmg_log:
				print("{0:15} {1:-12.1f} {2:-8.2f}%".format(dmg_type, dmg_val, dmg_val/tot*100))

			for x in all_stats:
				print(x.d)
		return tot

# raiden_weapons_normal = [skyward_spine(1), the_catch(5)]
raiden_weapons_normal = [the_catch(5)]
raiden_weapons_premium = [engulfing_lightning(1)]
raiden_chars_normal = [Raiden(w, 2, 220) for w in raiden_weapons_normal]
raiden_chars_premium = [Raiden(w, 2, 220) for w in raiden_weapons_premium] + [Raiden(w, 3, 220) for w in raiden_weapons_normal]

# yae_weapons_normal = [solar_pearl(5), widsith(5, 1/9, 1/9, 1/9)]
yae_weapons_normal = [solar_pearl(5)]
yae_weapons_premium = [kagura(1, 3, 1)]
yae_chars_normal = [Yae(w, 0, 240) for w in yae_weapons_normal]
yae_chars_premium = [Yae(w, 0, 240) for w in yae_weapons_premium] + [Yae(w, 1, 240) for w in yae_weapons_normal]

# xingqiu_weapons_normal = [sac_sword(5), lions_roar(5, 1)]
xingqiu_weapons_normal = [sac_sword(5)]
xingqiu_weapons_premium = [jade_cutter(1)]
xingqiu_chars_normal = [Xingqiu(w, 6, 250, 20) for w in xingqiu_weapons_normal]
xingqiu_chars_premium = [Xingqiu(w, 6, 250, 20) for w in xingqiu_weapons_premium]

bennett_weapons_normal = [favonius_sword(1)]
bennett_weapons_premium = [aquila_favonia(1)]
bennett_chars_normal = [Bennett(w, 5, 1) for w in bennett_weapons_normal]
bennett_chars_premium = [Bennett(w, 5, 1) for w in bennett_weapons_premium]

team_candidates = []
for x in raiden_chars_premium:
	for y in itertools.product(yae_chars_normal, xingqiu_chars_normal, bennett_chars_normal):
		z = list(y)
		team_candidates.append(RaidenYaeXingqiuBennett(tuple(z[:0] + [x] + z[0:])))

for x in yae_chars_premium:
	for y in itertools.product(raiden_chars_normal, xingqiu_chars_normal, bennett_chars_normal):
		z = list(y)
		team_candidates.append(RaidenYaeXingqiuBennett(tuple(z[:1] + [x] + z[1:])))

for x in xingqiu_chars_premium:
	for y in itertools.product(raiden_chars_normal, yae_chars_normal, bennett_chars_normal):
		z = list(y)
		team_candidates.append(RaidenYaeXingqiuBennett(tuple(z[:2] + [x] + z[2:])))

for x in bennett_chars_premium:
	for y in itertools.product(raiden_chars_normal, yae_chars_normal, xingqiu_chars_normal):
		z = list(y)
		team_candidates.append(RaidenYaeXingqiuBennett(tuple(z[:3] + [x] + z[3:])))

# team_candidates = [
# RaidenYaeXingqiuBennett((Raiden1_BP(the_catch(5)), Yae_BP(solar_pearl(5)), Xingqiu6_BP(sac_sword(5)), Bennett5_BP(favonius_sword(1)))),
# RaidenYaeXingqiuBennett((Raiden2_BP(the_catch(5)), Yae_BP(solar_pearl(5)), Xingqiu6_BP(sac_sword(5)), Bennett5_BP(favonius_sword(1)))),
# RaidenYaeXingqiuBennett((Raiden3_BP(the_catch(5)), Yae_BP(solar_pearl(5)), Xingqiu6_BP(sac_sword(5)), Bennett5_BP(favonius_sword(1)))),
# RaidenYaeXingqiuBennett((Raiden1_BP(engulfing_lightning(1)), Yae_BP(solar_pearl(5)), Xingqiu6_BP(sac_sword(5)), Bennett5_BP(favonius_sword(1)))),
# RaidenYaeXingqiuBennett((Raiden2_BP(engulfing_lightning(1)), Yae_BP(solar_pearl(5)), Xingqiu6_BP(sac_sword(5)), Bennett5_BP(favonius_sword(1)))),
# RaidenYaeXingqiuBennett((Raiden3_BP(engulfing_lightning(1)), Yae_BP(solar_pearl(5)), Xingqiu6_BP(sac_sword(5)), Bennett5_BP(favonius_sword(1)))),
# ]

scores_names = []
for team in team_candidates:
	team.optimize()
	print(team.name())
	team.score(True)
	for c, mains, subs in zip(team.chars, team.mains, team.subs):
		print(c.__class__.__name__)
		print(mains)
		print(subs)
	scores_names.append((team.score(), team.name()))

scores_names.sort()
scores_names.reverse()

for x in scores_names:
	print("{0:150s} {1:.0f}".format(x[1], x[0]))


