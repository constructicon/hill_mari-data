#!/usr/bin/env bash

for file in data/*.yml; do
    yamllint $file
done
