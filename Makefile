.PHONY: requirements

## Install Python Dependencies
requirements: test_environment
	pip install -r requirements.txt
