pyinstaller --add-data "cat.ico;." -F -w -i "cat.ico" "���� ���⭮�� �맮��.pyw"
xcopy "dist\*.exe" /y
rd /s /q build __pycache__ dist
del /f /s /q *.spec
#Pause