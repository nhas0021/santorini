import img_showcase
import tile_showcase
import iso_showcase


if __name__ == '__main__':
	print("Select a showcase:\n(1) Img\n(2) Tile\n(3) Iso\n")
	while 1:
		try:
			foo = int(input())
		except ValueError:
			print("Invalid Input")
			continue

		match foo:
			case 1:
				img_showcase.main()
			case 2:
				tile_showcase.main()
			case 3:
				iso_showcase.main()
			case _:
				print("Invalid Input")