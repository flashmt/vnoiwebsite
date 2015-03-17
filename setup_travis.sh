#!/bin/bash
cat << "EOF"
              _        _           _   
   __ _ _   _| |_ ___ | |__   ___ | |_ 
  / _` | | | | __/ _ \| '_ \ / _ \| __|
 | (_| | |_| | || (_) | |_) | (_) | |_ 
  \__,_|\__,_|\__\___/|_.__/ \___/ \__|
EOF

set -e
source ~/.bashrc

# Install python
virtualenv venv
source venv/bin/activate
pip install -r ./requirements.txt

# Ensure we are in the project directory
cd "$(dirname "$0")"
ruby -v

echo "********* Install dependencies"
cd functional_tests
gem install bundle
bundle install

