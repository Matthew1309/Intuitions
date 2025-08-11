#!/bin/bash

# Extract_audio.sh

# Usage:
# sh Extract_audio.sh link1 link2 ...

# Code:
for arg in "$@"; do
	# original command:
	# yt-dlp --extract-audio --audio-format mp3 --audio-quality 0 "$arg"
	trimmed_url="${arg%%&list*}"
	yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 "$trimmed_url"
done


