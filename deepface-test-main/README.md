### Install [CMake](https://cmake.org/) first

## Install:
```bash
pip install dlib deepface tf-keras pyinstaller
```

## Run:
```bash
py ./main.py
py ./api.py
```

## Build:
```bash
python -m PyInstaller --onefile -w main.py
python -m PyInstaller --onefile -w api.py
```
Place the "haarcascade_frontalface_default.xml" file in the same directory as the "main.exe" executable.
