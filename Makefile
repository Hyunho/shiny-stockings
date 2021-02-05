
image=hyunho/stocking

WORKING_DIR := $(shell pwd)

dev:
	docker build --tag="${image}:dev" --file "./builder/dev/Dockerfile" .
	docker run -it --rm -p 8080:8080 -v "${PWD}":/usr/src/app  "${image}:dev" bash

jupyter:
	@echo
