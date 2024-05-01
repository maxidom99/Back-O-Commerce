#!/bin/bash
clear
sudo chmod u+x back.sh 2>/dev/null
A=1
while [ $A -ne 0 ]
do
echo "🌐🔥 BIENVENIDO A GITHUB - O-COMMERCE 🔥🌐"
echo ""
echo "Qué desea hacer❓"
echo ""
echo "1. Pullear desde main"
echo "2. Pushear al main"
echo "3. Chequear ultimos Commits"
echo "4. Volver un Commit"
echo ""
echo "(0) Volver al Menú 🔙"
echo ""
read -p "Ingrese una opcion: " opc
case $opc in

1) clear
sh ./auto/GitPull.sh
;;
2) clear
sh ./auto/GitPush.sh
;;
3) clear
git log -n 5 --pretty=format:"%h - %ad - %an - %s" --date=short
echo ""
read -p "Presione Enter para volver..."
clear
;;
4) clear
function Revert() {
    read -p "Desea ver el historial de commits? (s/n) " res
    if [[ $res == "S" || $res == "s" ]];
    then
    git log -n 10 --pretty=format:"%h - %ad - %s" --date=short
    sleep 1
    read -p "Ingrese el ID del commit al que desea volver: " ID
    echo ""
    read -p "⚠️   ESTAS SEGURO DE LO QUE ESTAS HACIENDO? (s/[n]) ⚠️   " val
    val=${val:-n}
    if [[ $val == "S" || $val == "s" ]];
    then
    git revert "$ID"
    elif [[ $val == "N" || $val == "n" ]]; 
    then
    echo "Volviendo atras... 🔙"
    sleep 1
    else
    echo "Opcion incorrecta."
    sleep 1
    fi
    elif [[ $val == "N" || $val == "n" ]];
    then
    git revert "$ID"
    elif [[ $res == "N" || $res == "n" ]];
    then
    read -p "Ingrese el ID del commit al que desea volver: " ID
    git revert "$ID"
    else
    echo "Opcion incorrecta, intente nuevamente."
    sleep 1
    fi
}
Revert
;;

0)clear
echo "Volviendo al menú... 🔙"
sleep 0.7
A=0
;;

*) 
clear
echo "Opción incorrecta, intente nuevamente."
sleep 1
clear
;;

esac
done
