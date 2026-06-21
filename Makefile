PYTHON ?= python3

.DEFAULT_GOAL := help
.PHONY: help install validate charts build all clean

help: ## Show this help
	@echo "2026 Oklahoma Sooners CWS research — make targets:"
	@echo "  make install   Install Python dependencies (requirements.txt)"
	@echo "  make validate  Validate all datasets (schema, rows, confidence, sources)"
	@echo "  make charts    Regenerate the chart suite"
	@echo "  make build     Validate + charts + deterministic build manifest"
	@echo "  make all       Alias for 'make build'"
	@echo "  make clean     Remove build manifest and Python caches"

install: ## Install dependencies
	$(PYTHON) -m pip install -r requirements.txt

validate: ## Validate datasets
	$(PYTHON) scripts/validate_data.py

charts: ## Regenerate charts
	$(PYTHON) charts/make_charts.py

build: ## Full reproducible build (validate -> charts -> manifest)
	$(PYTHON) scripts/build_report_assets.py

all: build ## Rebuild everything

clean: ## Remove generated manifest and caches
	rm -f build_manifest.json
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
	find . -name "*.pyc" -delete
