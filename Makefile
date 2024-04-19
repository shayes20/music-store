ENTRYPOINT=main.py

.phony: clean run cloc

clean:
	find . -type d -name '__pycache__' -exec rm -rf {} +
	docker compose down

run:
	python $(ENTRYPOINT)

cloc:
	cloc . --exclude-dir=.venv,__pycache__