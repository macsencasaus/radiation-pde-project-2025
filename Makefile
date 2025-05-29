build:
	pip install -r requirements.txt
	cd web/frontend && npm install && npm run build
.PHONY: build

run:
	PYTHONPATH=. python3 web/backend/server.py
.PHONY: run
