import subprocess
import json
import re
from base64 import b64encode
from IPython.display import HTML, display


def get_video_details(filename):
  cmd = ['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', filename]
  result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  info = json.loads(result.stdout)

  # Get video stream
  video_stream = next(stream for stream in info['streams'] if stream['codec_type'] == 'video')

  # Get resolution
  width = int(video_stream['width'])
  height = int(video_stream['height'])
  resolution = width*height

  # Get fps
  fps = eval(video_stream['avg_frame_rate'])

  # Get length
  length = float(info['format']['duration'])

  return width, height, fps, length

def show_video(file_path):
  """Function to display video in Colab"""
  mp4 = open(file_path,'rb').read()
  data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
  width, _, _, _ = get_video_details(file_path)
  display(HTML("""
  <video controls width=%d>
      <source src="%s" type="video/mp4">
  </video>
  """ % (min(width, 1280), data_url)))

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)

    if hours > 0:
        return f'{hours}h {minutes}m {seconds}s'
    elif minutes > 0:
        return f'{minutes}m {seconds}s'
    else:
        return f'{seconds}s'

def get_input_length(filename):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def is_url(string):
    url_regex = re.compile(r'^(https?|ftp)://[^\s/$.?#].[^\s]*$')
    return bool(url_regex.match(string))

def g_colab():
    try:
        import google.colab
        return True
    except ImportError:
        return False
