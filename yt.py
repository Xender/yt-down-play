#!/usr/bin/env python

import sys
import subprocess

player_cmd = ['mpv', '--keep-open']

youtube_dl_destination_filename_msg_prefix = '[download] Destination: '

def spawn_player(filename):
	return subprocess.Popen(
		player_cmd + ['--',
			filename
		],
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

		for line in youtube_dl.stdout:
			sys.stdout.write(line)

			# 'If' here to prevent spawning multiple players playing\
			# simultaneously when downloading a playlist.
			# (This script is not intended for that anyway, but better safe than sorry.)
			if not video_filename_already_found:
				if line.startswith(youtube_dl_destination_filename_msg_prefix):
					video_filename = line[len(youtube_dl_destination_filename_msg_prefix) : -1] # -1 for trailing '\n'.
					video_filename_already_found = True

					spawn_player( video_filename+'.part' )

if __name__ == "__main__":
	main(sys.argv)
