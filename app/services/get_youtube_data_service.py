from app.services.youtube_services import YouTubeServices
from pytube import YouTube
import json


class GetYouTubeDataService(YouTubeServices):
    def __init__(self, url: str) -> None:
        super().__init__(url)

    def get_youtube_video_info(self):

        # Call the YouTube Data API to get video details
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics", id=self.video_id
        )
        response = request.execute()

        # Extract the required information from the response
        if response["items"]:
            video = response["items"][0]
            title = video["snippet"]["title"]
            description = video["snippet"]["description"]
            published_at = video["snippet"]["publishedAt"]
            view_count = video["statistics"].get("viewCount", "N/A")
            like_count = video["statistics"].get("likeCount", "N/A")
            comment_count = video["statistics"].get("commentCount", "N/A")

            video_info = {
                "Title": title,
                "Description": description,
                "Published At": published_at,
                "View Count": view_count,
                "Like Count": like_count,
                "Comment Count": comment_count,
            }

            return video_info
        else:
            print("No video found for the provided video ID.")
            return None

    def get_subtitles(self, language_code: str = "en"):
        # Initialize YouTube object
        yt = YouTube(self.video_url)

        # Get the caption track for the specified language
        caption = yt.captions.get_by_language_code(language_code)

        if not caption:
            print(f"No captions found for language code: {language_code}")
            return None

        # Convert the caption to XML format
        caption_xml = caption.xml_captions

        # Parse the XML to extract text, start, and duration
        import xml.etree.ElementTree as ET

        root = ET.fromstring(caption_xml)

        subtitles = []
        for elem in root.iter("text"):
            start = float(elem.attrib["start"])
            duration = float(elem.attrib["dur"])
            end = start + duration
            text = elem.text or ""

            subtitles.append(
                {"text": text, "start": start, "end": end, "duration": duration}
            )

        return subtitles

    def get_youtube_comments(self, max_results: int = 10):

        # Make the API call to get comments
        request = self.youtube.commentThreads().list(
            part="snippet",
            videoId=self.video_id,
            maxResults=max_results,
            textFormat="plainText",
        )

        response = request.execute()

        comments = []

        # Loop through the response to extract comments
        while request is not None:
            response = request.execute()

            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]
                comments.append(
                    {
                        "author": comment["authorDisplayName"],
                        "text": comment["textDisplay"],
                        "like_count": comment["likeCount"],
                        "published_at": comment["publishedAt"],
                    }
                )

            # Check if there is a next page token, then make the next request
            if "nextPageToken" in response:
                request = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=self.video_id,
                    maxResults=max_results,
                    textFormat="plainText",
                    pageToken=response["nextPageToken"],
                )
            else:
                request = None

        return comments

    def gather_youtube_data_and_save(self, language_code: str = "en"):

        # Get video information
        video_info = self.get_youtube_video_info()

        # Get subtitles
        subtitles = self.get_subtitles(language_code=language_code)

        # Get comments
        comments = self.get_youtube_comments()

        # Combine all data into one dictionary
        youtube_data = {
            "Video Information": video_info,
            "Subtitles": subtitles,
            "Comments": comments,
        }

        # Save the data as a JSON file
        with open(f"./output_db/{self.video_id}.json", "w") as outfile:
            json.dump(youtube_data, outfile, indent=4)

        print(f"Data saved to {self.video_id}.json")
