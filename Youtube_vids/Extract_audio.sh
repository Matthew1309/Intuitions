#!/bin/bash

# Extract_audio.sh

# Usage:
# sh Extract_audio.sh link1 link2 ...

# Code:
for arg in "$@"; do
	yt-dlp --extract-audio --audio-format mp3 --audio-quality 0 "$arg"
done


