#!/bin/sh
# Saca los cuadros clave: sh shots.sh [1 2 3 intro perdida final]  (el server tiene que estar en el 5331)
cd "$(dirname "$0")"; mkdir -p cuadros
for n in ${@:-1 2 3 intro perdida final}; do
  case $n in [0-9]) ui=0;; *) ui=1;; esac
  timeout 90 "/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --enable-gpu --use-angle=d3d11 --ignore-gpu-blocklist \
    --hide-scrollbars --window-size=1280,720 --virtual-time-budget=6000 \
    --screenshot="$(cygpath -w "$PWD")/cuadros/$n.png" "http://localhost:5331/?shot=$n&ui=$ui&mute=1" >/dev/null 2>&1
  echo "cuadro $n: $?"
done
