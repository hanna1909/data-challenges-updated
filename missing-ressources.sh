#!/bin/zsh

valid_urls=()
invalid_urls=()

echo "\nlooking for object urls in the content 👀"

# -r                          recursive
# -o                          only print matching part of the line
# -h                          do not print matching file name
# -I                          ignore binary files

# [a-z0-9.-]*                 aws bucket names accept lowercase letters, numbers, dots and hyphens
# [a-zA-Z0-9.%/_-]*           aws object names accept previous + uppercase letters, percents, slashes and underscores

# retrieve the list of aws s3 and gcs objects referenced in the content, ignores directories (ressources ending by /)
# https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/
# https://storage.googleapis.com/datascience-mlops/taxi-fare-ny/
# https://raw.githubusercontent.com/lewagon/data-images/master/decision-science/
objects=$(grep -rohI "https://\([a-z0-9.-]*.s3.amazonaws\|storage.googleapis\|raw.githubusercontent\).com/[a-zA-Z0-9.%=/_-]*" . | grep -E "[^/]$" | uniq)

echo "\nvaliding object urls 🧪"

for url in $(echo $objects)
do
  # checking whether objects exist
  if curl --output /dev/null --silent --head --fail "$url"; then
    echo "URL exists: $url 👌"
    valid_urls+=($url)
  else
    echo "URL does not exist: $url ❌"
    invalid_urls+=($url)
  fi
done

# print valid urls
echo "\nvalid urls: 👌"
for valid in $valid_urls
do
  echo $valid
done

# print invalid urls
echo "\ninvalid urls: ❌"
for invalid in $invalid_urls
do
  echo $invalid
done

# handle script return code
if [ ${#invalid_urls[@]} -eq 0 ]; then
else
  echo "missing objects referenced in the content 🤕"

  echo "\n👉 if the object is a directory, append a trailing slash to the object url:"
  echo "- ❌ invalid: ...://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny"
  echo "- ✅ valid: https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/"

  # fail script
  exit 1
fi
