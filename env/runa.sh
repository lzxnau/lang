#!/bin/bash

cd "$HOME"/pgit/lang || exit
source env/lang/bin/activate || exit

export CUDA_VISIBLE_DEVICES=""
export PYTHONUNBUFFERED=1
export TOKENIZERS_PARALLELISM="false"
export USER_AGENT="LangChain Jeff"
export PYTHONPATH="$HOME"/pgit/lang/src
python3.12 src/lang/test/test.py
