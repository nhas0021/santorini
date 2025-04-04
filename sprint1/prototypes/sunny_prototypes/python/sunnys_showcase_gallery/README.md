# Tkinter Prototype
- Run from this directory
	- Python paths are weird 

## Order of Creation
1. overlap
2. tile
3. iso

## Build Steps
1) `pip install pyinstaller` ([See More](https://pyinstaller.org/en/stable/index.html))
2)  Ensure current directory is `sunnys_showcase_gallery`
3) `pyinstaller .\showcase_selector.py --onedir --name 'Sunny_Prototype' --contents-directory 'Assets' --hidden-import=tkinter --add-data ./art:art`
4) (Optional) Run from cmd with error display `.\Sunny_Prototype.exe && pause`