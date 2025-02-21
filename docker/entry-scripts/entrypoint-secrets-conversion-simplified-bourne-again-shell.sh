#!/bin/bash
#
# Author: Benjamin P. Trachtenberg
# Version: 2025.2.20.001
#
# entrypoint-secrets-conversion-simplified-bourne-again-shell.sh
#
# This script scans all environment variables (via `env`) for any variable
# whose value is a file path starting with "/run/secrets/".
# For each match, it checks if the file exists, reads its content,
# and then sets the environment variable to that content (without exporting).
#
# Usage: This script is the Container entrypoint. You pass the CMD as arguments.
#        If the container is already using an entrypoint script, you can
#        chain it to this script.
#
# Example: exec /some-entrypoint-script.sh "$@"

# Loop over each environment variable.
while IFS='=' read -r var_name var_value; do
  # Check if the variable's value begins with /run/secrets/
  if [[ "$var_value" == /run/secrets/* ]]; then
    echo "Found variable '$var_name' referencing file '$var_value'"
    if [ -f "$var_value" ]; then
      # Read the file content using input redirection
      new_value=$(< "$var_value")
      # Escape any embedded double quotes in the new value
      escaped=$(printf "%s" "$new_value" | sed 's/"/\\"/g')
      # Set the variable to the new value in the current shell
      eval "$var_name=\"$escaped\""
      echo "Updated '$var_name' with contents from '$var_value'."
    else
      echo "Warning: File '$var_value' for variable '$var_name' not found." >&2
    fi
  fi
done < <(env)

# Execute the container's main command.
exec "$@"
