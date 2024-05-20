#!/usr/bin/env bash

set -e

if ! systemctl is-active postgresql.service &>/dev/null; then
    systemctl start postgresql.service
fi

mkdir --parents MyMovies/movies/static/movies/css
npm run gencss
