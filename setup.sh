#!/bin/bash
echo "Actualizando pip ..."
python3 -m pip install --upgrade pip

echo "Instalando dependencias del proyecto ..."
pip install -r requirements.txt

#instalaremos los hooks que estan en hooks/ a .git/hooks/
echo "Instalando hooks en .git/hooks/ ..."
cp hooks/commit-msg .git/hooks/commit-msg
cp hooks/pre-push .git/hooks/pre-push
cp hooks/pre-commit .git/hooks/pre-commit

#le damos permiso de ejecucion a los hooks creados
chmod +x .git/hooks/commit-msg
chmod +x .git/hooks/pre-push
chmod +x .git/hooks/pre-commit

echo "Hooks y dependencias instaladas correctamente"
