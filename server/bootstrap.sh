#!/bin/bash
set -e

BASEDIR="$(greadlink -f $(dirname $0))"
HSPROTO_DIR="$BASEDIR/hs-proto"
HSPROTO_URL="https://github.com/HearthSim/hs-proto.git"
PYPROTO_DIR="$BASEDIR/protos"

echo "Fetching data files from $HSPROTO_URL into $HSPROTO_DIR"

if [[ ! -e "$HSPROTO_DIR" ]]; then
	git clone "$HSPROTO_URL" "$HSPROTO_DIR"
else
	git -C "$HSPROTO_DIR" fetch &&
	git -C "$HSPROTO_DIR" reset --hard origin/master
fi

for proto in "$HSPROTO_DIR"/**/*.proto; do
	protoc -I "$HSPROTO_DIR" --python_out="$PYPROTO_DIR" $proto;
done
