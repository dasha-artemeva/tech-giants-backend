#!/bin/bash
VENV_PATH="$(poetry env info --path)/bin/activate"
source "$VENV_PATH"
export $(grep -v '^#' .env | xargs)
export PGPASSWORD="$DATABASE_PASSWORD"
alias pcmd="psql -U $DATABASE_USER -h $DATABASE_HOST -p $DATABASE_PORT -d postgres"
echo "Activated env"

