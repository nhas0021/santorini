pyinstaller .\App.py --onefile --name Santorini --contents-directory Resources --hidden-import=tkinter --add-data ./Assets:Assets --noconfirm
%SystemRoot%\explorer.exe ".\dist\"