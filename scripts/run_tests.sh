OMIT=--omit=*/venv/*,*/virtualenv/*,*/dist-packages/*

coverage run -a $OMIT manage.py test || exit 1;
