#!/bin/bash
clear
chmod u+x GitPush.sh 2>/dev/null

git add .
git status
sleep 1.1
read -p "¿Descripcion del Commit? " commit
git commit -m "$commit"
git push -u origin main
sleep 1.1
clear
