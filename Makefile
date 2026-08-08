.PHONY: help generate-assets check-structure check-docs check-names check-secrets status

help:
	@printf 'Luis Franca Portfolio - repository bootstrap targets\n'
	@printf '\n'
	@printf '  help             Show available targets\n'
	@printf '  generate-assets  Regenerate visual delivery derivatives from approved masters\n'
	@printf '  check-structure  Validate required top-level structure and .gitkeep markers\n'
	@printf '  check-docs       Validate presence of canonical normative documents\n'
	@printf '  check-names      Verify obsolete repository names and document paths are absent\n'
	@printf '  check-secrets    Search for accidentally committed secrets\n'
	@printf '  status           Show working directory, branch, Git status, remote origin\n'

generate-assets:
	@bash scripts/generate-assets.sh

GITKEEP_DIRS = docker nginx scripts .github/workflows \
	frontend/templates frontend/static/css frontend/static/js frontend/static/images frontend/static/fonts

STRUCTURE_FILES = backend/manage.py backend/config/settings/base.py tests/unit/test_settings.py

check-structure:
	@status=0; \
	for dir in $(GITKEEP_DIRS); do \
		if [ -d "$$dir" ] && [ -f "$$dir/.gitkeep" ]; then \
			printf 'PASS  %s/.gitkeep\n' "$$dir"; \
		else \
			printf 'FAIL  %s missing .gitkeep marker\n' "$$dir"; \
			status=1; \
		fi; \
	done; \
	for file in $(STRUCTURE_FILES); do \
		if [ -f "$$file" ]; then \
			printf 'PASS  %s\n' "$$file"; \
		else \
			printf 'FAIL  %s missing\n' "$$file"; \
			status=1; \
		fi; \
	done; \
	if [ $$status -eq 0 ]; then \
		printf 'PASS  repository structure complete\n'; \
	fi; \
	exit $$status

DOC_FILES = \
	docs/00-engineering-generation-standard.md \
	docs/01-product-brief.md \
	docs/02-technical-specification.md \
	docs/03-architecture.md \
	docs/04-api-and-data-contracts.md \
	docs/05-testing-and-acceptance.md \
	docs/06-deployment-and-operations.md \
	docs/adr/ADR-001-release-strategy.md \
	docs/adr/ADR-002-technology-stack.md \
	docs/adr/ADR-003-python-runtime-and-development-toolchain.md \
	docs/specs/SPEC-001-mvp-foundation.md \
	docs/specs/SPEC-002-contact-and-communication.md \
	docs/specs/SPEC-003-portfolio-and-projects.md \
	docs/specs/BASELINE-001.md

check-docs:
	@status=0; \
	for file in $(DOC_FILES); do \
		if [ -f "$$file" ]; then \
			printf 'PASS  %s\n' "$$file"; \
		else \
			printf 'FAIL  %s missing\n' "$$file"; \
			status=1; \
		fi; \
	done; \
	if [ $$status -eq 0 ]; then \
		printf 'PASS  all canonical documents present\n'; \
	fi; \
	exit $$status

check-names:
	@status=0; \
	if grep -RInE --exclude-dir=.git --exclude-dir=.venv --exclude-dir=.pytest_cache --exclude-dir=.mypy_cache --exclude-dir=.ruff_cache 'LF_[T]echnology_Information|LF [T]echnology|lf-[t]echnology-portfolio' .; then \
		printf 'FAIL  obsolete repository branding found\n'; \
		status=1; \
	fi; \
	if grep -RInE --exclude-dir=.git --exclude-dir=.venv --exclude-dir=.pytest_cache --exclude-dir=.mypy_cache --exclude-dir=.ruff_cache 'docs/adr/ADR-002 — [T]echnology Stack\.md|docs/specs/SPEC-001 — [M]VP Foundation\.md|docs/specs/SPEC-002 — [C]ontact & Communication\.md|docs/specs/SPEC-003 — [P]ortfolio & Projects\.md' .; then \
		printf 'FAIL  obsolete document-path form found\n'; \
		status=1; \
	fi; \
	if [ $$status -eq 0 ]; then \
		printf 'PASS  no obsolete repository names or document-path forms\n'; \
	fi; \
	exit $$status

check-secrets:
	@status=0; \
	tracked_env_files="$$( \
		git ls-files | \
		grep -E '(^|/)\.env($$|\.)' | \
		grep -vE '(^|/)\.env\.example$$' || true \
	)"; \
	if [ -z "$$tracked_env_files" ]; then \
		printf 'PASS  no forbidden environment files are tracked\n'; \
	else \
		printf 'FAIL  forbidden environment files are tracked:\n'; \
		printf '%s\n' "$$tracked_env_files"; \
		status=1; \
	fi; \
	secret_files="$$( \
		git grep -PIl -i \
			-e '(api[_-]?key|access[_-]?key|client[_-]?secret|secret[_-]?key|token|password|passwd|private[_-]?key|BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY)[[:space:]]*[:=][[:space:]]*(?!os\.environ|os\.getenv|env[a-z_]*\b)[^[:space:]]+' \
			-- ':!.env.example' 2>/dev/null \
	)"; \
	if [ -n "$$secret_files" ]; then \
		for f in $$secret_files; do \
			printf 'FAIL  potential secret detected in %s\n' "$$f"; \
		done; \
		status=1; \
	else \
		printf 'PASS  no potential secrets detected in tracked files\n'; \
	fi; \
	exit $$status

status:
	@printf 'working directory: %s\n' "$$(pwd)"; \
	printf 'active branch:     %s\n' "$$(git branch --show-current)"; \
	printf 'Git status:\n'; \
	git status; \
	printf 'remote origin:     %s\n' "$$(git remote get-url origin)"
