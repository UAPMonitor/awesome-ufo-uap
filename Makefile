.PHONY: help

help: ## Show this help
	@echo "Usage: make [target]"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Build the docker image
	docker-compose build

validate: ## Run docker-compose to validate the data
	@echo "Validating data..."
	docker-compose run --rm app python3 src/validate.py
	@echo
	@echo "Finished validating data"
	@echo

generate: validate ## Run docker-compose to generate the data
	@echo "Generating data..."
	docker-compose run --rm app
	@echo
	@mv .tools/dist/README.md .
	@echo "Done!"
