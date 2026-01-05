import os

ratesA = [0.5]

adv_rate_A = 0.15

committees = [10000]

rates = [0.25, 0.3, 0.33]

for rateA in ratesA:
	for committee in committees:
		for rate_lazy in rates:
			for rate_adv in rates:
				print(f"Running Weighted MonteCarlo with {rateA} {adv_rate_A} Committee {committee} Lazy: {rate_lazy} Adv: {rate_adv}	")
				os.system(f"./weighted_monte_carlo {rate_lazy} {rate_adv} {committee} {adv_rate_A} {rateA}")
