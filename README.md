python3.13 -m PyInstaller --clean -F -w --collect-data TKinterModernThemes -i chat.ico --add-data chat.ico:. main.py
python3.13 -m PyInstaller --clean -F server.py
