
from YT2AU import YouTube_Downloader

destination = r'C:\Users\Michael\Desktop\Spotify Music'
url = 'https://www.youtube.com/watch?v=mX8nBeajrho'


def main():
    YTD = YouTube_Downloader(destination)
    YTD.download(url=url, mode='single')


if __name__ == '__main__':
    main()