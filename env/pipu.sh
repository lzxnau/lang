#!/bin/bash

export PY=python3.12
export VENV=lang
export RPATH=$HOME/pgit/lang/env
export UNAME=$RPATH/$VENV/up.txt

cd "$RPATH" || exit

venv_install() {
  deactivate
  rm -rf $VENV
  $PY -m venv $VENV &&
    source $VENV/bin/activate &&
    pip install -r "$RPATH"/$VENV.txt && echo
}

venv_check() {
  source $VENV/bin/activate || venv_install
  pip list -o >$VENV/up.txt &&
    eval "$(python pack.py)" && echo
  echo "$VENV-->$PIP_CHANGES"
  if [ "$PIP_CHANGES" == "True" ]; then
    venv_install
  fi
  deactivate
}

venv_check
