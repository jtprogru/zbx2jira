.DEFAULT_GOAL := help

# Аргумент для `make run` — JSON-строка из Zabbix {ALERT.MESSAGE}
MSG ?=

.PHONY: help
help: ## Показать список доступных команд
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Установить зависимости (runtime + dev) в .venv через uv
	uv sync --dev

.PHONY: install-prod
install-prod: ## Установить только runtime-зависимости
	uv sync --no-dev

.PHONY: lock
lock: ## Пересобрать uv.lock
	uv lock

.PHONY: upgrade
upgrade: ## Обновить зависимости до последних совместимых версий
	uv lock --upgrade

.PHONY: lint
lint: ## Проверить код ruff
	uv run ruff check .

.PHONY: lint-fix
lint-fix: ## Исправить то, что ruff умеет чинить автоматически
	uv run ruff check --fix .

.PHONY: fmt
fmt: ## Отформатировать код ruff
	uv run ruff format .

.PHONY: fmt-check
fmt-check: ## Проверить форматирование без изменения файлов
	uv run ruff format --check .

.PHONY: run
run: ## Запустить приложение: make run MSG='<json>'
	uv run python main.py '$(MSG)'

.PHONY: clean
clean: ## Удалить виртуальное окружение и кэши
	rm -rf .venv
	find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.py[cod]' -delete 2>/dev/null || true
