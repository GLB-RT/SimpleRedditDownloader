import requests
import redvid
import os
import shutil
from moviepy import VideoFileClip, AudioFileClip
import re

class RedditVideoDownloader:
    def __init__(self, limit=10):
        self.limit = limit

    def fetch_reddit_links(self):
        url = "https://www.reddit.com/r/funny/top.json?t=week"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0'})
        
        if response.status_code == 200:
            data = response.json()
            video_links = []
            titles = []
            
            for post in data['data']['children']:
                post_data = post['data']
                
                if 'post_hint' in post_data and post_data['post_hint'] in ["hosted:video", "video"]:
                    if 'url' in post_data:
                        video_links.append(post_data['url'])
                        titles.append(post_data['title'])
            
            # Limit the number of links to download
            video_links = video_links[:self.limit]
            titles = titles[:self.limit]
            
            return video_links, titles
        else:
            print("Error fetching data.")
            return [], []

    def download_videos(self, link_list):
        for url in link_list:
            reddit = redvid.Downloader(max_q=True)
            reddit.url = url
            try:
                reddit.download()
            except Exception as e:
                print(f"Error downloading video: {e}")

    def get_temp_folder_paths(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        temp_dir = os.path.join(current_dir, "redvid_temp")
        
        if os.path.exists(temp_dir):
            return [f for f in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, f))]
        else:
            print("The 'redvid_temp' folder does not exist.")
            return []

    def sanitize_title(self, title):
        # Remove special characters
        title = re.sub(r'[^\w\s\.,:/]', '', title)
        
        # Replace dots and commas with underscores
        title = title.replace('.', '_').replace(',', '_')
        
        # Replace spaces with underscores
        title = title.replace(' ', '_')
        
        # Replace slashes and colons with underscores
        title = title.replace('/', '_').replace(':', '_')
        
        return title

    def merge_video_audio(self, folder_list, titles):
        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "redvid_temp")
        videos_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")
        
        if not os.path.exists(videos_dir):
            os.makedirs(videos_dir)
        
        for i, folder in enumerate(folder_list):
            folder_path = os.path.join(temp_dir, folder)
            
            if os.path.exists(folder_path):
                files = os.listdir(folder_path)
                
                audio_file = None
                video_file = None
                
                for file in files:
                    if file.endswith(('.m4a', '.wav', '.mp3')):
                        audio_file = file
                    elif file.endswith('.mp4'):
                        video_file = file
                
                if audio_file and video_file:
                    video_clip = VideoFileClip(os.path.join(folder_path, video_file)).without_audio()
                    audio_clip = AudioFileClip(os.path.join(folder_path, audio_file))
                    
                    final_clip = video_clip.with_audio(audio_clip)
                    
                    # Save file with a number
                    output_file = f"{i+1}.mp4"
                    output_path = os.path.join(videos_dir, output_file)
                    
                    final_clip.write_videofile(output_path)
                    
                    # Close files
                    video_clip.close()
                    audio_clip.close()
                    final_clip.close()
                    
                    print(f"Files in folder {folder} have been merged into {output_file}")
                    
                    # Delete folder
                    try:
                        shutil.rmtree(folder_path)
                        print(f"Folder {folder} has been deleted.")
                    except PermissionError:
                        print(f"Error deleting folder {folder}. The file is being used by another process.")
                else:
                    print(f"No audio and/or video files found in folder {folder}")
            else:
                print(f"Folder {folder} does not exist.")

    def delete_redvid_temp_folder(self):
        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "redvid_temp")
        
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                print("The 'redvid_temp' folder has been deleted.")
            except Exception as e:
                print(f"Error deleting the 'redvid_temp' folder: {e}")

    def run(self):
        links, titles = self.fetch_reddit_links()
        self.download_videos(links)
        folders = self.get_temp_folder_paths()
        self.merge_video_audio(folders, titles)
        self.delete_redvid_temp_folder()

# Use a limit of 5 videos
downloader = RedditVideoDownloader(limit=5)
downloader.run()
