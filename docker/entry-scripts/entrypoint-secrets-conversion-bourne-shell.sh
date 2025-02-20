#!/bin/sh
#
# Author: Benjamin P. Trachtenberg
# Version: 2025.2.20.001
#
# entrypoint-secrets-conversion-bourne-shell.sh
#
# This script scans all environment variables (as provided by `env`)
# for any whose value is in the form: $(cat /path/to/secret).
# For each match, it reads the referenced file and updates that variable
# with the file’s content.
#
# IMPORTANT: This script is written in Bourne shell, which is more portable
#            than Bash. However, it does not support the same advanced features as Bash.
#            Since it uses cat it spawns an extra process, which can be problematic in some cases.
#
# Finally, it execs the command passed to the container.
#
# Usage: This script is the Container entrypoint. You pass the CMD as arguments.
#        If the container is already using an entrypoint script, you can
#        chain it to this script.
#
# Example: exec /some-entrypoint-script.sh "$@"

# Loop over each environment variable.
env | while IFS='=' read -r name value; do
  # Use sed with extended regex to extract a file path if the variable's value matches the pattern:
  # either $(cat <file>) or $(< <file>)
  file=$(printf "%s" "$value" | sed -nE 's/^\$\((cat|<)[[:space:]]+([^)]*)\)$/\2/p')
  if [ -n "$file" ]; then
    echo "Found variable '$name' referencing file '$file'"
    if [ -f "$file" ]; then
      new_value=$(cat "$file")
      # Escape any embedded double quotes.
      escaped=$(printf "%s" "$new_value" | sed 's/"/\\"/g')
      # Update the variable in the current shell using eval.
      eval "export $name=\"$escaped\""
      echo "Updated '$name' with contents from '$file'."
    else
      echo "Warning: File '$file' for variable '$name' not found." >&2
    fi
  fi
done

# Execute the container's main command.
exec "$@"
