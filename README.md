# Groupic
## How to Set-Up in 5 Minutes:
```bash
git clone https://github.com/moshekan/groupic.git
cd groupic
virtualenv groupic-env
source groupic-env/bin/activate
pip install -r requirements.txt
```
## Pushing back to github:
```bash
git pull
git add -p
git commit -m "INSERT UPDATES HERE"
git push origin master
```


## Setup additional packages
```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y git ruby python-pip python-virtualenv libpq-dev python-dev
sudo apt-get install -y postgresql postgresql-contrib
sudo apt-get install -y libncurses-dev
wget -O- https://toolbelt.heroku.com/install.sh | sh
```

## For OSX

```bash
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" # install homebrew
brew install postgresql
```
