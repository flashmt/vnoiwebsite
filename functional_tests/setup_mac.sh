#!/bin/bash
cat << "EOF"
              _        _           _   
   __ _ _   _| |_ ___ | |__   ___ | |_ 
  / _` | | | | __/ _ \| '_ \ / _ \| __|
 | (_| | |_| | || (_) | |_) | (_) | |_ 
  \__,_|\__,_|\__\___/|_.__/ \___/ \__|
EOF

green='\033[0;32m'
NC='\033[0m'

green_tick="${green}√${NC}"

# install brew
if which brew >/dev/null; then
    echo -e "[${green_tick}] brew exists"
else
    echo installing brew
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi

for pkg in rbenv ruby-build; do
    if brew list -1 | grep -q "^${pkg}\$"; then
        echo -e "[${green_tick}] Package '$pkg' is installed"
    else
        echo "installing '$pkg'"
        brew install $pkg
    fi
done

echo checking .bashrc
if grep -Fxq 'eval "$(rbenv init -)"' ~/.bashrc
then
    echo -e "[${green_tick}] found"
else
    echo 'eval "$(rbenv init -)"'>>~/.bashrc
    echo -e "[${green_tick}] setting .bashrc"
fi

echo checking .zshrc
if grep -Fxq 'eval "$(rbenv init -)"' ~/.zshrc
then
    echo -e "[${green_tick}] found"
else
    echo 'eval "$(rbenv init -)"'>>~/.zshrc
    echo -e "[${green_tick}] setting .zshrc"
fi

source ~/.bashrc
rbenv install 2.1.2
rbenv rehash
sudo gem install bundler
gem uninstall nokogiri
xcode-select --install
sudo gem install nokogiri
sudo gem install bundler
rbenv rehash
bundle install
rbenv rehash
echo -e "[${green_tick}] autobot install success"
