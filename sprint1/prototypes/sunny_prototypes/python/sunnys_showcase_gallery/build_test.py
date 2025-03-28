if __name__ == '__main__':
	print("Select a showcase:\n(1) Img\n(2) Tile\n(3) Iso\n")
	while 1:
		try:
			foo = int(input())
		except ValueError:
			print("Invalid Input")
			continue

		print("HELLO WORLD!")