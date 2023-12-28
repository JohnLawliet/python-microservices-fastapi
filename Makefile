install:
  #install dependencies
  python -m pip install --upgrade pip
  pip install pytest pylint black
format:
  #format code with black
  black **.py
lint:
  #install pylint
test:
  #create test with pytest