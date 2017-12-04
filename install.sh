
echo 'Installiere Command line Tools...'
xcode-select --install
sleep 1
osascript <<EOD
  tell application "System Events"
    tell process "Install Command Line Developer Tools"
      keystroke return
      click button "Agree" of window "License Agreement"
    end tell
  end tell
EOD
sleep 3

if test ! $(which brew)
then echo 'Installiere Homebrew...'
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi 
sleep 3

sudo chown -R $(whoami) /usr/local/var/homebrew
sudo chown -R $USER:admin /usr/local

echo 'Installiere Git...'
brew install git

echo 'erweiterung des Paths'
sleep 3

echo 'export PATH=/usr/local/bin:$PATH' >> ~/.bash_profile

echo 'Installiere Python3...'
sleep 3

brew install python3
brew upgrade python3

echo 'erstelle Projects'
if [ ! -d "~/Projects" ];
then  mkdir ~/Projects 
fi

cd ~/Projects

echo 'erstelle virtuelle Umgebung'
python3.6 -m venv WPF_Scraper
source WPF_Scraper/bin/activate
pip install scrapy
pip install flask
pip install flask_restful
pip install requests

echo 'Erstelle Aliase in die .profile'
cat .profile >> ~/.profile 
