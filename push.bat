@echo off
git add .
echo.
set/p comentario = ¿Comentario para el commit?
echo.
git commit -m "aa"
git push
pause>nul
exit