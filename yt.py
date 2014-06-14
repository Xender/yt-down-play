#!/usr/bin/env python

import sys
import subprocess

player = b'mpv'
player_stdout = subprocess.DEVNULL
player_stderr = subprocess.DEVNULL

youtube_dl_destination_filename_msg_prefix = b'[download] Destination: '

def spawn_player(filenames):
	pass

def main(argv):
	youtube_dl = subprocess.Popen(
		['youtube-dl'] + argv[1:],
		stdout = subprocess.PIPE
		)

	with youtube_dl: #???
		video_filename_already_found = False

		for line in youtube_dl.stdout:
			sys.stdout.write(line.decode())

			if not video_filename_already_found:
				print("Filename not yet found.", file=sys.stderr)
				if line.startswith(youtube_dl_destination_filename_msg_prefix):
					video_filename = line[len(youtube_dl_destination_filename_msg_prefix) : ]
					video_filename_already_found = True

					print("!!! Filename prefix match. Filename ==", repr(video_filename), file=sys.stderr)

					subprocess.Popen(
						[ player, '--',
							video_filename,
							video_filename+'.part' # First check if file is already downloaded, if not, use the .part file
						],
						stdin = subprocess.DEVNULL,
						stdout = player_stdout,
						stderr = player_stderr)
						# TODO Should start_new_session=True be also used above?

if __name__ == "__main__":

	if False:
		player_stdout = ''
		player_stderr = ''
	main(sys.argv)
