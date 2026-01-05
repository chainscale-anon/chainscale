import os

committees = [500, 1000, 5000, 10000]

rates = [0.25, 0.3, 0.33]

for committee in committees:
	for rate_lazy in rates:
		for rate_adv in rates:
			print(f"Running MonteCarlo with Committee {committee} Lazy: {rate_lazy} Adv: {rate_adv}	")
			os.system(f"./monte_carlo {rate_lazy} {rate_adv} {committee}")
