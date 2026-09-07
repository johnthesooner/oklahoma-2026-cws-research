PYTHON ?= python3

.DEFAULT_GOAL := help
.PHONY: help install validate charts build softball championships football test social site all clean

help: ## Show this help
	@echo "2026 Oklahoma Sooners CWS research — make targets:"
	@echo "  make install   Install Python dependencies (requirements.txt)"
	@echo "  make validate  Validate all datasets (schema, rows, confidence, sources)"
	@echo "  make charts    Regenerate the chart suite"
	@echo "  make build     Validate + charts + deterministic build manifest"
	@echo "  make football  Validate + rebuild the football eras module"
	@echo "  make test      Run the offline pytest suite (football module)"
	@echo "  make football-crosscheck  Verify the football game log against ESPN (network)"
	@echo "  make all       Rebuild everything (baseball + softball + championships + football)"
	@echo "  make clean     Remove build manifest and Python caches"

install: ## Install dependencies
	$(PYTHON) -m pip install -r requirements.txt

validate: ## Validate datasets
	$(PYTHON) scripts/validate_data.py

charts: ## Regenerate charts
	$(PYTHON) charts/make_charts.py

build: ## Full reproducible build (validate -> charts -> manifest)
	$(PYTHON) scripts/build_report_assets.py

softball: ## Validate + rebuild the softball module
	$(PYTHON) softball/scripts/validate_softball.py
	$(PYTHON) softball/scripts/analyze_softball.py

championships: ## Validate + rebuild the all-sports championships module
	$(PYTHON) championships/scripts/validate_championships.py
	$(PYTHON) championships/scripts/analyze_championships.py

football: ## Validate + rebuild the football eras module (1999-2025)
	$(PYTHON) football/scripts/validate_football.py
	$(PYTHON) football/scripts/analyze_football.py

football-crosscheck: ## Second-source check of the football game log against ESPN's schedule API (network; cached)
	$(PYTHON) football/scripts/crosscheck_espn.py

test: ## Offline unit + dataset-consistency tests
	$(PYTHON) -m pytest football/tests -q

social: ## Generate social-media assets (carousel + GIF) from the championships data
	$(PYTHON) social/scripts/make_social_assets.py

site: ## Build the public landing page's web-optimized assets (site/assets/)
	$(PYTHON) site/build_site.py

all: build softball championships football ## Rebuild everything (baseball + softball + championships + football)

clean: ## Remove generated manifest and caches
	rm -f build_manifest.json
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
	find . -name "*.pyc" -delete
