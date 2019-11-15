del "dist\*.gz" /f
del "dist\*.whl" /f
python setup.py sdist bdist_wheel