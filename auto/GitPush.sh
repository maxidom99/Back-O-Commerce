#!/bin/bash
clear
chmod u+x GitPush.sh 2>/dev/null

echo " 😺 GITHUB (PUSH) - O-COMMERCE 😺 "
echo "==================================="
echo "       1) Pushear O-Commerce"
echo "       2) Pushear Backend"
echo "       3) Pushear Frontend"
echo ""
read -p "---> " opc

if [ $opc -eq 1 ]; then
#PUSH BACKEND
git add .
git status
sleep 1.1
read -p "¿Descripcion del Commit (BACKEND)? " commitback
git commit -m "$commitback"
git push -u origin main
sleep 1.1
clear

#PUSH FRONTEND
cd ../o-commerce/FrontO-Commerce
git add .
git status
sleep 1.1
read -p "¿Descripcion del Commit (FRONTEND)? " commitfront
git commit -m "$commitfront"
git push -u origin main
sleep 1.1
clear

elif [ $opc -eq 2 ]; then
git add .
git status
sleep 1.1
read -p "¿Descripcion del Commit (BACKEND)? " commitback
git commit -m "$commitback"
git push -u origin main
sleep 1.1
clear

elif [ $opc -eq 3 ]; then
cd ../o-commerce/FrontO-Commerce
git add .
git status
sleep 1.1
read -p "¿Descripcion del Commit (FRONTEND)? " commitfront
git commit -m "$commitfront"
git push -u origin main
sleep 1.1
clear

fi