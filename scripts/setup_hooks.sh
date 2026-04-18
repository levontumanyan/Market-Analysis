#!/bin/bash
# .git/hooks/pre-commit

echo "Running pre-commit checks..."
make check

if [ $? -ne 0 ]; then
    echo "Checks failed! Commit aborted."
    exit 1
fi

echo "All checks passed."
exit 0
