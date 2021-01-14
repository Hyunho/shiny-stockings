
image=hyunho/stocking

WORKING_DIR := $(shell pwd)

dev:
	docker build --tag="${image}:dev" --file "./builder/dev/Dockerfile" .
	docker run -it --rm  -v "${PWD}":/usr/src/app  "${image}:dev" bash
