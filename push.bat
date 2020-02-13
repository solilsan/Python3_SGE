@echo off
git add .
echo.
set /p msg=¿Comentario para el commit?
echo.
echo "%msg%"
git commit -m "%msg%"
git push
echo.
echo Push completo.
pause>nul
exit