#!/bin/sh
# Usage: KEY=fieldname VALUE=newvalue EDITOR=mirrorbits-edit-script mirrorbits edit ...

if [ -z "$KEY" ] || [ -z "$VALUE" ]; then
    echo "Error: KEY and VALUE environment variables must be set" >&2
    exit 1
fi

sed -i "s/^${KEY}: .*/${KEY}: ${VALUE}/" "$1"
