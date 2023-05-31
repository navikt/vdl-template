#!/bin/bash
use="n"
if [ $DBT_USR ]; then
  echo "Current user:" $DBT_USR
  echo "Do you still want to use the current user? Y/n"
  read  use
  echo ""
  use=${use:-y}
fi

if [ $use = 'n' ]; then
  echo "Username:"
  read username
  export DBT_USR=$username
fi

if [ $use = 'n' ]; then
  echo "Use SSO? y/N"
  read sso
  sso=${sso:-n}
fi

if [ $sso = 'y' ]; then
  export DBT_TARGET='sso'
fi

if [ $sso = 'n' ]; then
  unset DBT_TARGET
fi

if [[ $use = 'n' || $sso = 'n' && -z ${DBT_PWD+x} ]]; then
  echo "Password:"
  read -s password
  echo ""
  export DBT_PWD=$password
fi

use="n"
if [ $<PROJECT_DB> ]; then
  echo "Current DB:" $<PROJECT_DB>
  echo "Do you still want use the current database? Y/n"
  read use
  echo ""
  use=${use:-y}
fi

prod_db=<prod database name>

if [[ -z ${<PROJECT_DB>+x} || $use = 'n' ]]; then
  echo "Choose a database:"
  select db in $prod_db dev_$prod_db dev_"$prod_db"_$USER other; do
    break;
  done
  if [ $db = 'other' ]; then
    echo Database:
    read db
    echo ""
  fi
  export <PROJECT_DB>=$db
fi

recreate_db=n
if [ $<PROJECT_DB> != $prod_db ]; then
  echo "Do you want to create / recreate the database: $<PROJECT_DB>? y/N"
  read recreate_db
  echo ""
  recreate_db=${recreate_db:-n}
fi

if [ $recreate_db = 'y' ]; then
  echo "Here is script you can run in snowflake:"
  echo ""
  echo "create or replace database $<PROJECT_DB> clone $prod_db;"
  echo "grant usage on database $<PROJECT_DB> to role "$prod_db"_loader;"
  echo "grant usage on database $<PROJECT_DB> to role "$prod_db"_transformer;"
  echo "grant usage on database $<PROJECT_DB> to role "$prod_db"_reporter;"
fi
