def NC(numConv, width, height, hidden, kernel, poolSize1, poolSize2):
	size = [0, 0, 0]
	size[0] = (width - kernel + 1) / poolSize1
	size[1] = (height - kernel + 1) / poolSize1
	size[2] = hidden

	for i in range(numLayer - 1):
		size[0] = int((size[0] - kernel + 1) / poolSize2)
		size[1] = int((size[1] - kernel + 1) / poolSize2)
		size[2] = hidden * (2**(i+1))

	total = size[0]*size[1]*size[2]

	return total
