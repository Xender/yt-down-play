#!/usr/bin/env python3

import sys
import os
import subprocess

player_cmd = ['mpv', '--keep-open']
# --keep-open handles unbuffered video,
# but when mpv cannot detect a valid header
# it exeits even with that option.
# Care of that is taken later.

youtube_dl_destination_filename_msg_prefix = '[download] Destination: '

def spawn_player(filename):
	return subprocess.Popen(
		player_cmd + ['--', filename],
		stdin = subprocess.DEVNULL
	)
	# TODO Should start_new_session=True be also used above?

def main(argv):
	with subprocess.Popen(
		['youtube-dl'] + argv[1:],
		universal_newlines = True,
		stdout = subprocess.PIPE
	) as youtube_dl:

		video_filename_already_found = False
		headers_already_buffered     = False

		for line in youtube_dl.stdout:
			sys.stdout.write(line)

			# 'If' here to prevent spawning multiple players playing\
			# simultaneously when downloading a playlist.
			# (This script is not intended for that anyway, but better safe than sorry.)
			if not video_filename_already_found:
				if line.startswith(youtube_dl_destination_filename_msg_prefix):
					video_filename_already_found = True
					video_filename = line[len(youtube_dl_destination_filename_msg_prefix) : -1]+'.part' # -1 for trailing '\n'.

			else: # == Video filename already found (double negative).
				if not headers_already_buffered:
					if os.path.getsize(video_filename) >= 64*1024: # Arbitrary headers size guess. Now testing 64k
						headers_already_buffered = True
						spawn_player(video_filename)


if __name__ == "__main__":
	main(sys.argv)
