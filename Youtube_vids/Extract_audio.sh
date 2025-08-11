#!/bin/bash

# Extract_audio.sh

# Usage:
# sh Extract_audio.sh link1 link2 ...

# Code:
for arg in "$@"; do
	# yt-dlp --extract-audio --audio-format mp3 --audio-quality 0 "$arg"
	yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 --ffmpeg-location "$(which ffmpeg)" "$arg"
done


