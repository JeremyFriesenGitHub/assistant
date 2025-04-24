#!/bin/bash

set -e

CMD=$1
MESSAGE=$2

ALEMBIC_CFG="infrastructure/db/alembic.ini"

if [ "$CMD" == "revision" ]; then
  if [ -z "$MESSAGE" ]; then
    echo "🛑 Please provide a migration message"
    echo "Usage: ./scripts/migrate.sh revision 'add new table'"
    exit 1
  fi
  alembic -c $ALEMBIC_CFG revision --autogenerate -m "$MESSAGE"
elif [ "$CMD" == "upgrade" ]; then
  alembic -c $ALEMBIC_CFG upgrade head
elif [ "$CMD" == "downgrade" ]; then
  alembic -c $ALEMBIC_CFG downgrade -1
else
  echo "🛠 Usage:"
  echo "  ./scripts/migrate.sh revision 'message'   # create a new migration"
  echo "  ./scripts/migrate.sh upgrade              # apply latest migration"
  echo "  ./scripts/migrate.sh downgrade            # roll back one migration"
fi
