@echo off
git add .
set /p msg=Comentario para el commit? 
git commit -m "%msg%"
git push
exit