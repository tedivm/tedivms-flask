#!/usr/bin/env bash

REQUIREMENTS_FILE=$1

while read p; do
  if [[ -z "${p// }" ]];then
    continue
  fi
  if [[ "${p// }" == \#* ]];then
    continue
  fi

  count=$(echo ${p// } | wc -m)
  if (( count < 3 )); then
    continue
  fi

  program=$(echo $p | cut -d= -f1)
  curr_version=$(cat ./requirements.txt | grep "${program}==" | cut -d'=' -f3 | sed 's/[^0-9.]*//g')
  PACKAGE_JSON_URL="https://pypi.python.org/pypi/${program}/json"
  version=$(curl -L -s "$PACKAGE_JSON_URL" | jq  -r '.releases | keys | .[]' | sed '/^[^[:alpha:]]*$/!d' | sort -V | tail -1 | sed 's/[^0-9.]*//g' )

  if [ "$curr_version" != "$version" ]; then
    echo "Updating requirements for ${program} from ${curr_version} to ${version}."
    sed -i -e "s/${program}==.*/${program}==${version}/g" $REQUIREMENTS_FILE
  fi

done < $REQUIREMENTS_FILE

# OSX Creates a backup file.
rm -f "${REQUIREMENTS_FILE}-e"
