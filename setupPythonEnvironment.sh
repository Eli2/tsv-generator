#!/bin/bash
#Unofficial Bash Strict Mode
set -euo pipefail
IFS=$'\n\t'

# Dependencies:
# Ubuntu: python3-venv

PYENV_DIRECTORY='py3env'

install_python_dependencies() {
  # The activate script expects PS1
  # wich failes with 'Strict Mode'
  # create a dummy
  PS1=''
  export PS1
  
  . "$PYENV_DIRECTORY/bin/activate"
  pip install faker humanfriendly progressbar2
  deactivate
}

print_help() {
  echo "Enter with: source $PYENV_DIRECTORY/bin/activate"
  echo "Exit with:  deactivate"
}

if [ ! -d "$PYENV_DIRECTORY" ]; then
  echo "Creating venv at: $PYENV_DIRECTORY"
  virtualenv -p python3 "$PYENV_DIRECTORY"
  echo "Installing dependencies ..."
  install_python_dependencies
  print_help
else
  echo "Venv already exists, nothing to do..."
  print_help
fi
