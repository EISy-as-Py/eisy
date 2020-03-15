def NC(numConvLayer, width, height, firstHidden, kernel, poolSize):
	size = [0, 0, 0]
	for i in range(numConvLayer):
		width = int((width - kernel + 1) / poolSize)
		height = int((height - kernel + 1) / poolSize)
		size[0] = width
		size[1] = height
		size[2] = firstHidden*(2**i)

	print(size)
	total = size[0]*size[1]*size[2]
	return total
