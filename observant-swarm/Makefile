# Observant Swarm Python library
PROJECT=observant-swarm

BUILD=build
OUT=out

.PHONY: dist
dist:
	mkdir -p $(BUILD) $(OUT)
	( cd src; python3 setup.py egg_info --egg-base ../$(BUILD) sdist --dist-dir=../$(OUT) )

requirements.txt: FORCE
	pip freeze > requirements.txt


env:
	sudo apt-get install libgirepository1.0-dev gstreamer1.0-tools
	mkdir -p env
	virtualenv --prompt="$(PROJECT)" -p python3 env



.PHONY: FORCE
update-env: FORCE
	pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf $(BUILD) $(OUT)
	find . -iname '*.pyc' -delete
	find . -iname '__pycache__' -delete

.PHONY: distclean
distclean: clean
	rm -rf env
