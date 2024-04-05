import streamlit as st
import bs4
import os
import subprocess
import threading
from video_utils import join_videos
import openai 

api_key = ""

st.set_page_config(page_title="Video Maker", page_icon=":clapper:")

st.title("Video Maker")

background_color = st.color_picker('Pick a background color', '#3498db')

st.session_state['content'] = ''

# card1 = st.text_area('Text for card 1' , value='hello world !!!')
card2 = st.text_area('Text for card 2' , value='hey there !!!')
image_upload = st.file_uploader('Upload Image', type=['png','jpg','jpeg'], accept_multiple_files=False)
user_image_url = None
if image_upload is not None:
    user_image_url = 'tmp_user_image.png'
    image_upload.seek(0)
    with open(user_image_url, 'wb') as outf:
        outf.write(image_upload.read())



width = st.number_input('Width',  value=1080)
height = st.number_input('Height', value=1920)



def make_header(resolution, html_path):
    tmp_path = os.path.join('temp', os.path.basename(html_path))
    with open(html_path) as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt)


    try:
        soup.find(id='background-color').attrs['style'] = f'background-color: {background_color};'
        # soup.find(id='card1').string = card1 
        soup.find(id='card2').string = card2
        if user_image_url is not None:
            soup.find(id='card1').attrs['src'] =  os.path.join(os.getcwd(), user_image_url)

    except Exception as e:
        pass


    title_html = soup.prettify()
    with open(tmp_path, 'w') as outf:
        outf.write(title_html)



def runProcess(exe):    
    subprocess.Popen(exe, stdout=subprocess.PIPE, shell=True).stdout.readlines()

threads = []

if st.button('Make Video'):
    #remove files in output folder
    cmd = ["rm", "-rf", "output/*"]
    base_html_folder = r'D:\auto_poster'
    clips_name = ['zoom', '3d_rotate' ]

    # video_name = [ r'D:\auto_poster\3d_rotate\3d_rotate.html' , r'D:\auto_poster\zoomin\zoom.html' ]

    for i, clip in enumerate(clips_name):
        make_header(resolution=(width, height), html_path=os.path.join(base_html_folder, clip, clip+'.html'))
        cmd = ["gsap-video-export", f"temp/{clip}.html", "-t", "tl", "-o", f"output/{i}_{clip}.mp4"]
        thread = threading.Thread(target=runProcess, args=(cmd,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    join_videos()
    video_file = open('final.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)
    


