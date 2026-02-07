AGENTS_DIR := $(HOME)/.agents/skills
CLAUDE_DIR := $(HOME)/.claude/skills
SKILL_DIRS := $(shell find . -maxdepth 2 -name 'SKILL.md' -exec dirname {} \;)

.PHONY: link

link:
	@mkdir -p $(AGENTS_DIR) $(CLAUDE_DIR)
	@for skill in $(SKILL_DIRS); do \
		name=$$(basename $$skill); \
		src="$$(pwd)/$$name"; \
		for dir in $(AGENTS_DIR) $(CLAUDE_DIR); do \
			target="$$dir/$$name"; \
			if [ -L "$$target" ]; then \
				rm "$$target"; \
			fi; \
			ln -s "$$src" "$$target"; \
			echo "Linked: $$name -> $$target"; \
		done; \
	done
