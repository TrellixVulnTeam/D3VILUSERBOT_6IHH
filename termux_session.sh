clear
echo "
╭━━━┳━━━┳╮╱╱╭┳━━┳╮╱╱╭━━╮╭━━━┳━━━━╮
╰╮╭╮┃╭━╮┃╰╮╭╯┣┫┣┫┃╱╱┃╭╮┃┃╭━╮┃╭╮╭╮┃
╱┃┃┃┣╯╭╯┣╮┃┃╭╯┃┃┃┃╱╱┃╰╯╰┫┃╱┃┣╯┃┃╰╯
╱┃┃┃┣╮╰╮┃┃╰╯┃╱┃┃┃┃╱╭┫╭━╮┃┃╱┃┃╱┃┃
╭╯╰╯┃╰━╯┃╰╮╭╯╭┫┣┫╰━╯┃╰━╯┃╰━╯┃╱┃┃
╰━━━┻━━━╯╱╰╯╱╰━━┻━━━┻━━━┻━━━╯╱╰╯
"
# Termux session string generator for TeleBot
echo Starting dependency installation in 5 seconds...
sleep 5
apt-get update
apt-get upgrade -y
pkg upgrade -y
pkg install python wget -y
wget https://raw.githubusercontent.com/D3KRISH/D3vilUserbot/main/d3vil_string.py
pip install telethon
python d3vil_string.py
