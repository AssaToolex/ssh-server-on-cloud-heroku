#

.PHONY: pip_install_all
# vim:ft=make

pip_install_all: pip_install_cpython3 pip_install_pypy3

pip_install_cpython3:
	pip3 install -r requirements.txt

pip_install_pypy3:
	pypy3 -m pip install -r requirements.txt
