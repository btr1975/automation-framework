#!/bin/bash
#
# Author: Benjamin P. Trachtenberg
# Version: 2025.2.20.001
#
# entrypoint-secrets-conversion-bourne-again-shell.sh
#
# This script iterates through all environment variables (via `env`)
# and finds any whose value matches the pattern:
#   $(cat <file>)
# or
#   $(< <file>)
#
# For each match, it extracts <file>, checks if it exists, reads its content,
# and updates the variable accordingly.
#
# Usage: This script is the Container entrypoint. You pass the CMD as arguments.
#        If the container is already using an entrypoint script, you can
#        chain it to this script.
#
# Example: exec /some-entrypoint-script.sh "$@"

# Loop over each environment variable.
while IFS='=' read -r var_name var_value; do
  # This regex matches either 'cat' or '<' followed by one or more spaces and a file path.
  if [[ "$var_value" =~ ^\$\(\s*(cat|<)\s+([^)]*)\s*\)$ ]]; then
    secret_file="${BASH_REMATCH[2]}"
    echo "Found variable '$var_name' referencing file '$secret_file'"
    if [ -f "$secret_file" ]; then
      new_value=$(< "$secret_file")
      export "$var_name=$new_value"
      echo "Updated '$var_name' with contents from '$secret_file'."
    else
      echo "File '$secret_file' for variable '$var_name' not found."
    fi
  fi
done < <(env)

# Execute the container's main command.
exec "$@"
