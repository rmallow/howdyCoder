#!/bin/sh
curl -LJO https://github.com/indygreg/python-build-standalone/releases/download/20230726/cpython-3.10.12+20230726-x86_64-apple-darwin-install_only.tar.gz
tar -xvf cpython-3.10.12+20230726-x86_64-apple-darwin-install_only.tar.gz
rm -rf /Users/${USER}/Library/Application\ Support/HowdyCoder/
mkdir /Users/${USER}/Library/Application\ Support/HowdyCoder/
cp -r python /Users/${USER}/Library/Application\ Support/HowdyCoder/
/Users/${USER}/Library/Application\ Support/HowdyCoder/python/bin/python3.10 -m ensurepip

/Users/${USER}/Library/Application\ Support/HowdyCoder/python/bin/python3.10 -m pip install virtualenv

/Users/${USER}/Library/Application\ Support/HowdyCoder/python/bin/python3.10 -m virtualenv /Users/${USER}/Library/Application\ Support/HowdyCoder/env
source /Users/${USER}/Library/Application\ Support/HowdyCoder/env/bin/activate
python -m pip install -r ${DSTROOT}/HowdyCoder.app/Contents/Resources/requirements.txt

chmod -R 775 /Users/${USER}/Library/Application\ Support/HowdyCoder/
cd /Users/${USER}/Library/Application\ Support/HowdyCoder/env/bin/
ln -s python3.10 HowdyCoder