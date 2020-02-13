@echo off
git add .
echo.
set /p msg=¿Comentario para el commit?
echo.
git commit -m "%msg%"
git push
echo.
echo Push completo.
exit