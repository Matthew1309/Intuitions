This runs off of the github https://github.com/yt-dlp/yt-dlp

## Installation
1. Make a conda env with python 3.7+ (mine is 3.11)
2. `pip install -U yt-dlp`
3. Download `ffmpeg` from https://github.com/yt-dlp/FFmpeg-Builds#ffmpeg-static-auto-builds
4. Unzip the downloaded folder
5. Find your conda env's bin, mine was in `C:\Users\mattk\anaconda3\Library\bin`
then put the unzipped bin contents (3 items ffmpeg ffplay ffsomething) into the conda bin.

## Usage
This command here
`yt-dlp --extract-audio --audio-format mp3 --audio-quality 0 "youtube.url"`
will download audio as mp3 with decent video titles.

To automate this and make it slightly easier I made the `Extract_video.sh` script.
To use
1. Activate conda env
2. `./Extract_video.sh youtube.url1 youtube.url2 youtube.url3 ...`

