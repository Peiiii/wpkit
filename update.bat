del "dist\*.gz" /f
del "dist\*.whl" /f
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*