from abc import ABC
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs


class YouTubeServices(ABC):
    def __init__(self, url: str) -> None:
        super().__init__()
        self.api_key = self.read_api_key("youtube_api_key.txt")
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.video_url = url
        self.video_id = self.get_video_id_from_url(url=url)

    def get_video_id_from_url(self, url: str) -> str:
        # Parse the URL
        parsed_url = urlparse(url)

        # Check if the URL is a standard YouTube video link with a 'v' parameter
        if "v" in parse_qs(parsed_url.query):
            # Extract the video ID from the 'v' parameter
            video_id = parse_qs(parsed_url.query).get("v")
            return video_id[0]  # Return the first (and only) video ID

        # Check if the URL is a YouTube Shorts link
        elif "shorts" in parsed_url.path:
            # Extract the video ID from the path (e.g., '/shorts/cACYxEflIaI')
            video_id = parsed_url.path.split("/")[-1]
            return video_id

        else:
            raise ValueError("No video ID found in the URL")

    def read_api_key(self, file_path: str) -> str:
        try:
            with open(file_path, "r") as file:
                api_key = (
                    file.readline().strip()
                )  # Read the first line and strip any extra whitespace
            if not api_key:
                raise ValueError("API key file is empty.")
            return api_key
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {file_path} was not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while reading the API key: {e}")
