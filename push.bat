@echo off
git add .
echo.
set/p comentario = ¿Comentario para el commit?
echo.
git commit -m " & %comentario% & "
git push
echo.
echo Push completo.
pause>nul
exit