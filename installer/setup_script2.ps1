wget https://bootstrap.pypa.io/get-pip.py -o get-pip.py
mv python-3.10.2-embed-amd64\python310._pth python-3.10.2-embed-amd64\python310.pth
mkdir python-3.10.2-embed-amd64\DLLs
python-3.10.2-embed-amd64\python.exe get-pip.py

python-3.10.2-embed-amd64\python.exe -m pip install virtualenv

python-3.10.2-embed-amd64\python.exe -m virtualenv env
cp python-3.10.2-embed-amd64\python310.zip env\Scripts\