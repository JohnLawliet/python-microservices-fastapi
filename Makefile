install:
  	#install dependencies
  	pip install --upgrade pip &&\
		pip install -r requirements.txt
format:
  #format code with black
  	black **.py
lint:
  #install pylint
test:
  #create test with pytest
all: install lint test format