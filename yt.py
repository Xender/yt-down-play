#!/usr/bin/env python

import sys
import subprocess

player_cmd = ['mpv', '--keep-open']

youtube_dl_destination_filename_msg_prefix = '[download] Destination: '

def main(argv):
	youtube_dl = subprocess.Popen(
		['youtube-dl'] + argv[1:],
		universal_newlines = True,
		stdout = subprocess.PIPE
		)

	with youtube_dl:
		video_filename_already_found = False

		for line in youtube_dl.stdout:
			sys.stdout.write(line)

			if not video_filename_already_found:
				if line.startswith(youtube_dl_destination_filename_msg_prefix):
					video_filename = line[len(youtube_dl_destination_filename_msg_prefix) : -1] # -1 for trailing '\n'.
					video_filename_already_found = True

					subprocess.Popen(
						player_cmd + ['--',
							video_filename+'.part'
						],
						stdin = subprocess.DEVNULL)
						# TODO Should start_new_session=True be also used above?

if __name__ == "__main__":
	main(sys.argv)
