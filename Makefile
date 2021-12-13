all:
	lint

lint:
	isort . --py 39 --skip botenv
	black .