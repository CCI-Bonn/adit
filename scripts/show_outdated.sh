#!/usr/bin/env bash

poetry show --outdated | grep --file=<(poetry show --tree | grep '^\w' | sed 's/^\([^ ]*\).*/^\1/')