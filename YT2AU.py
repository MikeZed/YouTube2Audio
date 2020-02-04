

import moviepy.editor as mp
import pytube
import os

CHARS_TO_REMOVE = ['~', '.', '\'', '|', ':']


class YouTube_Downloader:
    # Creates an Youtube Video Downloader
    # that can Download and Convert Videos

    def __init__(self, destination, convert=True, file_format='mp3'):

        self.destination = destination
        self.tmp = os.path.join(destination, 'tmp')

        self.format = file_format
        self.convert = convert

        if not os.path.exists(self.destination):
            os.mkdir(self.destination)

    def download(self, url, mode='single', playlist_slice=None):
        # Downloads a Single Video, Multiple Videos or a Playlist

        if mode == 'single':
            self.download_and_convert(url)

        elif mode == 'multiple':
            self.download_from_urls(url)

        elif mode == 'playlist':
            self.download_playlist(url, playlist_slice)

        else:
            raise ValueError('Unknown Mode!')

    def download_playlist(self, playlist_url, playlist_slice=None):
        # Downloads a Playlist

        playlist = pytube.Playlist(playlist_url)

        playlist.populate_video_urls()

        urls = playlist.video_urls

        if playlist_slice is not None:
            urls = urls[playlist_slice[0] - 1: playlist_slice[1]]

        self.download_from_urls(urls)

    def download_from_urls(self, urls):
        # Downloads Multiple Videos

        for url in urls:
            self.download_and_convert(url)

    def download_and_convert(self, url):
        # Downloads a Single Video and Possibly Converts it to Another Type

        youtube_obj = pytube.YouTube(url)

        stream = youtube_obj.streams.filter(file_extension='mp4').first()

        title = youtube_obj.title
        file_type = stream.subtype

        downloaded_title = title

        for char in CHARS_TO_REMOVE:  # after downloading, video name won't contain any characters from CHARS_TO_REMOVE
            if char in downloaded_title:
                downloaded_title = downloaded_title.replace(char, '')

        video_path = os.path.join(self.destination, '{}.{}'.format(downloaded_title, file_type))

        converted_path = os.path.join(self.destination, '{}.{}'.format(downloaded_title, self.format))

        if not (os.path.exists(video_path) and stream.filesize == os.path.getsize(video_path)):
            # check if file already exists and fully downloaded

            print("Downloading '{}' from {}".format(title, url))

            stream.download(self.destination)

            print("Download Complete.")

        if self.convert:
            # if self.convert is True, converts the video to the requested type

            if not os.path.exists(converted_path):
                clip = mp.VideoFileClip(video_path)
                clip.audio.write_audiofile(converted_path)

                clip.reader.close()
                clip.audio.reader.close_proc()

            os.remove(video_path)
