#!/bin/sh
curl -LJO https://github.com/indygreg/python-build-standalone/releases/download/20230726/cpython-3.10.12+20230726-x86_64-apple-darwin-install_only.tar.gz
tar -xvf cpython-3.10.12+20230726-x86_64-apple-darwin-install_only.tar.gz
cp -r python ${DSTROOT}/HowdyCoder.app/Contents/Resources
${DSTROOT}/HowdyCoder.app/Contents/Resources/python/bin/python3.10 -m ensurepip

${DSTROOT}/HowdyCoder.app/Contents/Resources/python/bin/python3.10 -m pip install virtualenv

${DSTROOT}/HowdyCoder.app/Contents/Resources/python/bin/python3.10 -m virtualenv ${DSTROOT}/HowdyCoder.app/Contents/Resources/env
source ${DSTROOT}/HowdyCoder.app/Contents/Resources/env/bin/activate
python -m pip install -r ${DSTROOT}/HowdyCoder.app/Contents/Resources/requirements.txt