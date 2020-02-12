# https://stackoverflow.com/questions/2214575/passing-arguments-to-make-run
# If the first argument is "add_pattern"...
ifeq (add_pattern,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

TEST=pipenv run python3 pill_calendar.py test

ADD=pipenv run python3 pill_calendar.py add_pattern

PLAN=pipenv run python3 pill_calendar.py plan

APPLY=pipenv run python3 pill_calendar.py apply

HELP=pipenv run python3 pill_calendar.py help

test:
	$(TEST)

add_pattern:
	@$(ADD) $(RUN_ARGS)

plan:
	@$(PLAN)

apply:
	@$(APPLY)

help:
	@$(HELP)
