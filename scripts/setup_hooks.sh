#!/bin/bash
# .git/hooks/pre-commit

echo "Running pre-commit checks..."

# Only check, don't fix. This ensures the commit only contains what was staged.
make lint
LINT_EXIT=$?

make test
TEST_EXIT=$?

if [ $LINT_EXIT -ne 0 ] || [ $TEST_EXIT -ne 0 ]; then
	echo "Checks failed! Please run 'make format' and fix errors before committing."
	exit 1
fi

echo "All checks passed."
exit 0
