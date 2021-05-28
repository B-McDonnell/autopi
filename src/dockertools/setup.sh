#!/usr/bin/env bash

# if there is no file at DOCKER_HW_ID_PATH, fill it with random bytes
if [ ! -f $DOCKER_HW_ID_PATH ]; then
	hwid_hash=$(head --bytes 32 /dev/random | sha1sum | cut -d ' ' -f 1)

	echo $hwid_hash >> $DOCKER_HW_ID_PATH
	echo $hwid_hash >> $DOCKER_HW_ID_PATH
	echo $hwid_hash >> $DOCKER_HW_ID_PATH
	echo $hwid_hash >> $DOCKER_HW_ID_PATH
fi

