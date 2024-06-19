#!/bin/bash
sudo chmod u+x docker.sh 2>/dev/null

A=1
clear
while [ $A -ne 0 ]
do
clear
echo "🌐🔥 BIENVENIDO A DOCKER - O-COMMERCE 🔥🌐"
echo ""
echo "Qué desea hacer❓"
echo ""
echo "1. Restaurar Back y BD"
echo "2. Restaurar Back"
echo "3. Detener Back y BD"
echo ""
echo "(0) Volver al Menú 🔙"
echo ""
read -p "Ingrese una opcion: " opc

case $opc in

1) clear
function Restaurar {
    docker stop backend-app-1
    docker stop backend-db-1

    docker rm backend-app-1
    docker rm backend-db-1

    echo " ✅ Back y BD restaurado correctamente ✅ "
    sleep 1.1
}
Restaurar
;;

2) 
clear
function RestaurarBack {
    cd ./venv
    docker stop backend-app-1
    docker rm backend-app-1
    docker rmi backend-app-1
    docker-compose up -d
    clear
    cd ..
    echo " ✅ Back restaurado correctamente ✅"
    sleep 1.1
} 
RestaurarBack
;;

3) clear
    docker stop backend-app-1
    docker stop backend-db-1
echo ""
echo " 🛑 Backend y BD detenidos 🛑"
sleep 1.1
;;

0) clear
echo "Volviendo al menú... 🔙"
sleep 0.7
A=0
;;

*) clear
echo "Opción incorrecta."
sleep 0.7
;;
esac
done
