@echo off
git add .
echo.
set /p msg=Comentario para el commit? 
echo.
git commit -m "%msg%"
echo.
git push
exit