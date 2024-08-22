from app.get_youtube_data_service import GetYouTubeDataService

# Example usage:
video_id = "dQw4w9WgXcQ"  # Replace with your YouTube video ID
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with your YouTube video URL
language_code = "en"  # Replace with the desired language code for subtitles
api_key = "YOUR_YOUTUBE_API_KEY"  # Replace with your YouTube Data API key
output_file = "youtube_data.json"  # Replace with your desired output file name


youtube_service = GetYouTubeDataService(url=video_url).gather_youtube_data_and_save()