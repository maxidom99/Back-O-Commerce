#!/bin/bash
clear

echo " 😺 GITHUB (PULL) - O-COMMERCE 😺 "
echo "==================================="
echo "       1) Pullear O-Commerce"
echo "       2) Pullear Backend"
echo "       3) Pullear Frontend"
echo ""
read -p "---> " opc

if [ $opc -eq 1 ]; then
git pull origin main
sleep 0.6
cd ../o-commerce/FrontO-Commerce
git pull origin main
sleep 0.6
elif [ $opc -eq 2 ]; then
git pull origin main
sleep 0.6
elif [ $opc -eq 3 ]; then
cd ../o-commerce/FrontO-Commerce
git pull origin main
sleep 0.6
fi
sleep 1.2
clear