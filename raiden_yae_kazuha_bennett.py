from util import *
from char_weapon_bps import *
from collections import defaultdict

class RaidenYaeKazuhaBennett(Team):
	def __init__(self, chars):
		super().__init__(chars)

	def score(self, dbg=False):
		raiden, yae, kazuha, bennett = self.chars
		all_stats = self.get_stats()
		raiden_stats, yae_stats, kazuha_stats, bennett_stats = all_stats
		# assume buffs cannot buff buffs

		# artifact bonuses
		raiden_stats.d['er'] += 20 # other effect hardcoded into q dmg
		yae_stats.d['atkp'] += 18 + 18
		kazuha_stats.d['swirlp'] += 60 # ignore anemo dmg
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




	    # Raiden E - Kazuha E to swirl - Yae triple E - Yae Q - Yae triple E - Kazuha Q + E - Bennett Burst + E - Raiden Q - 3x N5 in Q form
		
		tot = 0
		base_res = 10
		electro_res = 10

		global_.dbg = dbg
		global_.dmg_log = [] if dbg else None

		# Raiden E

		tot += raiden.dmg_e(raiden_stats, base_res, -15, 12, False)

		# START Raiden E buff - lasts forever
		for c, s in zip(self.chars, all_stats):
			s.d['qp'] += c.q_cost * 0.3

		# Kazuha E

		tot += kazuha.dmg_e(kazuha_stats, base_res, electro_res)

		# START Kazuha VV and dmgp buff last forever
		electro_res = -15
		# snapshot kazuha em
		for s in all_stats:
			s.d['dmgp'] += kazuha_stats.d['em'] * 0.04

		# Yae Ex3 Q Ex3

		tot += yae.dmg_e(yae_stats, electro_res, 4/3, 3)
		tot += yae.dmg_q(yae_stats, electro_res, 3)

		if dbg:
			print(yae_stats)

		# Kazuha Q + E

		tot += kazuha.dmg_q(kazuha_stats, electro_res)
		tot += kazuha.dmg_e(kazuha_stats, electro_res, electro_res)

		# START Kazuha freedom sworn, 100% uptime until the end

		if 'freedom_sworn' in kazuha.weapon:
			for i, s in enumerate(all_stats):
				all_stats[i] = s + kazuha.weapon['freedom_sworn']
				raiden_stats, yae_stats, kazuha_stats, bennett_stats = all_stats

		# Yae Ex3 Q Ex3

		tot += yae.dmg_e(yae_stats, electro_res, 16/3, 3)

		# Bennett Q + E

		# START Bennett Q atk buff and 4NO buff, last forever
		# assume bennett c5
		for s in all_stats:
			s.d['atkf'] += bennett.q_atkf_buff(bennett_stats)
			s.d['atkp'] += 20

		# Raiden E continued
		tot += raiden.dmg_e(raiden_stats, electro_res, electro_res, ticks=10, in_q=True)

		# Raiden Q + (N5)x3

		tot += raiden.dmg_q(raiden_stats, electro_res, 3)

		if dbg:
			global_.dmg_log.append(("total", tot))
			for dmg_type, dmg_val in global_.dmg_log:
				print("{0:15} {1:-12.1f} {2:-8.2f}%".format(dmg_type, dmg_val, dmg_val/tot*100))

			# for x in all_stats:
			# 	print(x.d)
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

kazuha_weapons_normal = [iron_sting(1, 0)]
kazuha_weapons_premium = [freedom_sworn(1, 1)]
kazuha_chars_normal = [Kazuha(w, 0, 180) for w in kazuha_weapons_normal]
kazuha_chars_premium = [Kazuha(w, 0, 180) for w in kazuha_weapons_premium]

bennett_weapons_normal = [favonius_sword(1)]
bennett_weapons_premium = [aquila_favonia(1)]
bennett_chars_normal = [Bennett(w, 5, 1) for w in bennett_weapons_normal]
bennett_chars_premium = [Bennett(w, 5, 1) for w in bennett_weapons_premium]

# team_candidates = []
# for x in raiden_chars_premium:
# 	for y in itertools.product(yae_chars_normal, kazuha_chars_normal, bennett_chars_normal):
# 		z = list(y)
# 		team_candidates.append(RaidenYaeKazuhaBennett(tuple(z[:0] + [x] + z[0:])))

# for x in yae_chars_premium:
# 	for y in itertools.product(raiden_chars_normal, kazuha_chars_normal, bennett_chars_normal):
# 		z = list(y)
# 		team_candidates.append(RaidenYaeKazuhaBennett(tuple(z[:1] + [x] + z[1:])))

# for x in kazuha_chars_premium:
# 	for y in itertools.product(raiden_chars_normal, yae_chars_normal, bennett_chars_normal):
# 		z = list(y)
# 		team_candidates.append(RaidenYaeKazuhaBennett(tuple(z[:2] + [x] + z[2:])))

# for x in bennett_chars_premium:
# 	for y in itertools.product(raiden_chars_normal, yae_chars_normal, kazuha_chars_normal):
# 		z = list(y)
# 		team_candidates.append(RaidenYaeKazuhaBennett(tuple(z[:3] + [x] + z[3:])))

team_candidates = [RaidenYaeKazuhaBennett((raiden_chars_normal[0], yae_chars_normal[0], kazuha_chars_normal[0], bennett_chars_normal[0]))]

scores_names = []
for team in team_candidates:
	team.optimize()
	print(team.name())
	team.score(True)
	for c, mains, subs in zip(team.chars, team.mains, team.subs):
		print(c.name())
		print(mains)
		print(subs)
	scores_names.append((team.score(), team.name()))

scores_names.sort()
scores_names.reverse()

for x in scores_names:
	print("{0:150s} {1:.0f}".format(x[1], x[0]))

for x in scores_names:
	print(x[0]/scores_names[0][0]*100)

