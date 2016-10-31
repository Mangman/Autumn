with open("1.fq") as f:
	for line in f:
		for i in range(0,5):
			print next(f)
			next(f)
			next(f)
			next(f)
		break