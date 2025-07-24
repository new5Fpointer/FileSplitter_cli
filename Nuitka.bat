python -m nuitka --standalone --onefile ^
       --msvc=latest ^
       --no-deployment-flag=self-execution ^
       --include-package=chardet ^
       --output-dir=dist ^
       --output-filename=FileSplitter_cli.exe ^
       main.py
pause
