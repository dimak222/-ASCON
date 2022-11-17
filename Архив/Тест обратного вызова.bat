pyinstaller --add-data "cat.ico;." -F -w -i "cat.ico" "Тест обратного вызова.pyw"
xcopy "dist\*.exe" /y
rd /s /q build __pycache__ dist
del /f /s /q *.spec
#Pause