#!/usr/bin/env bash

for file in data/*.yml; do
    yamllint --no-warnings --config-file yamllint-config.yml $file
done
