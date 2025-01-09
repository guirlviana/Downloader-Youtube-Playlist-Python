from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytube import YouTube, Playlist
import os
from threading import Thread


class PlaylistDownloader:
    def __init__(self, playlist_path: str, folder_path: str) -> None:
        self.playlist_path = playlist_path
        self.folder_path = folder_path

    def extract_urls(self):
        """Extract individual URLs from the playlist."""
        return Playlist(self.playlist_path)

    def sanitize_filename(self, title: str) -> str:
        """Replace special characters in filenames."""
        invalid_chars = {'|', '>', '<', '?', '*', ':', '/', '\\'}
        return ''.join(' ' if char in invalid_chars else char for char in title)

    def download(self, links):
        """Download the playlist videos as audio files."""
        for link in links:
            try:
                yt = YouTube(link)
                sanitized_title = self.sanitize_filename(yt.title)
                print(f"Downloading: {sanitized_title}")
                yt.streams.filter(only_audio=True).first().download(
                    output_path=self.folder_path,
                    filename=sanitized_title
                )
                print("Video downloaded successfully.")
            except Exception as e:
                print(f"Error downloading video: {e}")

    def convert(self, files):
        """Convert MP4 files to MP3."""
        for file in files:
            root, ext = os.path.splitext(file)
            if ext == ".mp4":
                mp4_path = os.path.join(self.folder_path, file)
                mp3_path = os.path.join(self.folder_path, f"{root}.mp3")
                try:
                    with AudioFileClip(mp4_path) as audio:
                        audio.write_audiofile(mp3_path)
                    os.remove(mp4_path)
                    print(f"Converted: {file} -> {root}.mp3")
                except Exception as e:
                    print(f"Error converting file {file}: {e}")

    @staticmethod
    def divide_list(items, chunk_size):
        """Divide a list into chunks."""
        return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

    def get_mp4_in_folder(self):
        """Get MP4 files in the folder."""
        return [file for file in os.listdir(self.folder_path) if file.endswith(".mp4")]


def main():
    # Update with your playlist URL and download folder path
    playlist_url = "YOUR_PLAYLIST_URL"
    download_folder = r"YOUR_DOWNLOAD_FOLDER"

    downloader = PlaylistDownloader(
        playlist_path=playlist_url, folder_path=download_folder)

    # Extract and prepare URLs
    playlist_links = list(downloader.extract_urls())
    divided_links = downloader.divide_list(
        playlist_links, len(playlist_links) // 2)

    # Download the playlist using threads
    threads = [
        Thread(target=downloader.download, args=(divided_links[0],)),
        Thread(target=downloader.download, args=(divided_links[1],))
    ]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Get MP4 files and prepare for conversion
    mp4_files = downloader.get_mp4_in_folder()
    divided_files = downloader.divide_list(mp4_files, len(mp4_files) // 2)

    # Convert MP4 to MP3 using threads
    convert_threads = [
        Thread(target=downloader.convert, args=(divided_files[0],)),
        Thread(target=downloader.convert, args=(divided_files[1],))
    ]

    for thread in convert_threads:
        thread.start()
    for thread in convert_threads:
        thread.join()

    print("All Done! :)")


if __name__ == "__main__":
    main()
