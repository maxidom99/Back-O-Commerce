#!/bin/bash
clear
sudo chmod u+x GitPush.sh
cd ../../
git add .
git status
sleep 3
read -p "¿Nombre del Commit? " commit
git commit -m "$commit"
git push -u origin main
sleep 2
clear
