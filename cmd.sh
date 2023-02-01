#!/bin/zsh

set -e

if [[ $1 == "restart" ]]; then
  docker-compose restart "$2"
elif [[ $1 == "test" ]]; then
  docker-compose run --rm app sh -c "python manage.py test"
elif [[ $1 == "reset" ]]; then
  docker-compose down && docker-compose up -d --build --force-recreate
else
  echo "argument: restart, test"
fi