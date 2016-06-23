#curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
curl -O https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
curl -O https://bootstrap.pypa.io/get-pip.py
python ez_setup.py  
python get-pip.py
pip install --upgrade setuptools
pip install requests
pip install paramiko
pip install pycrypto
pip install ecdsa
