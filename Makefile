.PHONY: help validate build compile security ci bundle
.DEFAULT_GOAL := help

help:
	@echo "Targets:"
	@echo "  validate  - Validate XML and phyphox files (xmllint + phyphox_validate.py)"
	@echo "  build    - Rebuild *.phyphox from src/phyphox/*.phyphox.xml"
	@echo "  compile  - Compile Arduino sketch (arduino-cli, no upload)"
	@echo "  security - Secret scan, dependency pin check, minimal SAST"
	@echo "  ci       - Run validate, build, compile, security"
	@echo "  bundle   - Build *.phyphox and zip to phyphox-experiments.zip"

validate:
	./scripts/validate-xml.sh

build:
	./scripts/build-phyphox.sh

compile:
	./scripts/compile-arduino.sh

security:
	./scripts/secret-scan.sh
	./scripts/deps-scan.sh
	./scripts/sast-minimal.sh

ci: validate build compile security

bundle: build
	@zip -q -j phyphox-experiments.zip *.phyphox && echo "Created phyphox-experiments.zip"
