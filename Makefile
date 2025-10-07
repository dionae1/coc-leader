.PHONY: start env

start:
	--zsh -c "source .venv/bin/activate && python -m main"

env:
	--zsh -c "source .venv/bin/activate"