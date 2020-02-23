# https://stackoverflow.com/questions/2214575/passing-arguments-to-make-run
# If the first argument is "add_pattern"...
ifeq (add_pattern,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

TEST=pipenv run pytest --cov . -vv

DEV=pipenv run python3 pill_calendar.py dev

CLEAN=rm Calendar.csv.2*

ADD_PATTERN=pipenv run python3 pill_calendar.py add_pattern

ADD_TEST=pipenv run python3 pill_calendar.py add_test

PLAN=pipenv run python3 pill_calendar.py plan

APPLY=pipenv run python3 pill_calendar.py apply

HELP=pipenv run python3 pill_calendar.py help

test:
	$(TEST)

dev:
	$(DEV)

clean:
	$(CLEAN)

add_pattern:
	@$(ADD_PATTERN) $(RUN_ARGS)

add_test:
	@$(ADD_TEST)

plan:
	@$(PLAN)

apply:
	@$(APPLY)

help:
	@$(HELP)
