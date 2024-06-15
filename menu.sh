#!/bin/bash

directorio_principal=$(pwd)

function show_menu {
    clear
    echo "╔══════════════════════════════════════════════════╗"
    echo "║   🤖 BIENVENIDO AL MENÚ DE AUTOMATIZACIÓN 🤖     ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo ""
    echo "           Descubra el mundo de O-Commerce          "
    echo ""
    echo "1. GitHub"
    echo "2. Docker"
    echo "3. O-COMMERCE"
    echo ""
    echo "(0) Salir"
    echo ""
    read -p "Ingrese una opción: " opc
}

A=1

while [ $A -ne 0 ]; do
    show_menu

    case $opc in
        1)
            clear
            bash ./auto/github.sh
            ;;
        2)
            clear
            bash ./auto/docker.sh
            ;;
        3) 
            clear
            function WWE {
                cd ../o-commerce/FrontO-Commerce
                sleep 1
                echo " 😀 Front iniciado 😀"
                sleep 1.5
                npm run dev
            }

            function WWE+Back {
                cd ./venv
                docker-compose up -d
                sleep 1
                echo " 🔌 Back iniciado 🔌"
                sleep 1.5
                cd ../../o-commerce/FrontO-Commerce
                echo " 😀 Front iniciado 😀"
                sleep 1.5
		        npm i
                npm run dev
            }
            
            function Back {
                cd ./venv
                docker-compose up -d
                sleep 1
                echo " 🔌 Back iniciado 🔌"
                sleep 1
            }

           echo "Seleccione una opción:"
        echo "(1) SOLO 💻 FRONTEND 💻 (npm run dev)"
        echo "(2) SOLO 🔌 BACKEND 🔌 (Docker)"
        echo "(3) 🔌 BACKEND 🔌 y 💻 FRONTEND 💻 (Docker y npm run dev)"
        echo ""
        echo "(0) Volver al menu principal..."
        echo ""
        read -p "Ingrese una opción: " var
        if [ "$var" == "1" ]; then
            clear
            WWE
        cd "$directorio_principal"
        elif [ "$var" == "2" ]; then
            clear
            Back
        elif [ "$var" == "3" ]; then
            clear
            WWE+Back
        cd "$directorio_principal"
        elif [ "$var" == "0" ]; then
            clear
        cd "/auto"
        else
            sleep 0.1
            clear
            echo "Opción incorrecta, por favor seleccione 1 o 2."
            sleep 2
        fi
        ;;
        0)
            clear
            echo " 🔚 Saliendo del menú... 🔚"
            sleep 1.5
            A=0
            ;;
        *)
            clear
            echo "Opción incorrecta, intente nuevamente."
            sleep 1.5
            ;;
    esac
done
