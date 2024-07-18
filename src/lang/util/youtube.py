"""
Smart Platform Project: youtube module.

Version: 2024.07.18.01
"""

from pathlib import Path

from yt_dlp import YoutubeDL


class YTMgt:
    """YouTube Management Class."""

    Base_Path: Path = Path("/home/jliu/pgit/lang/out")

    @staticmethod
    def download_video(
        video_url: str,
        video_path: Path,
        file_name: str,
    ) -> None:
        """Download one video clip from YouTube."""
        try:
            ydl_opts = {
                "outtmpl": f"{str(video_path)}/{file_name}.%(ext)s",
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            print("YouTube video clip downloading is complete!")
        except Exception as e:
            print(f"YouTube video clip download error:\n{e}")


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=-tS9A2cxNM0"
    name = "song1"
    path = YTMgt.Base_Path
    YTMgt.download_video(url, path, name)
