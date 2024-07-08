#!/bin/bash

export PY=python3.12
export VENV=lang
export RPATH=$HOME/pgit/lang/env
export UNAME=$RPATH/$VENV/up.txt

cd $RPATH || exit

venv_install() {
    deactivate; \
    rm -rf $VENV; \
    $PY -m venv $VENV || exit
    source $VENV/bin/activate
    pip install -r $RPATH/$VENV.txt || exit
}

venv_check() {
    source $VENV/bin/activate || venv_install
    pip list -o > $VENV/up.txt

    eval "$(python pack.py)" || exit
    echo "$PIP_CHANGES-->$VENV"
    if [ "$PIP_CHANGES" == "True" ]; then
        venv_install
    fi
    deactivate || exit
}

venv_check || exit
