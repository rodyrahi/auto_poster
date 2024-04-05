import moviepy.editor as mp
import os

def join_videos():
    output_path = "output"

    clips_path = os.listdir(output_path)
    clips_path.sort()

    ## load all clips

    clips = []

    for clip_path in clips_path:
        clips.append(mp.VideoFileClip(os.path.join(output_path, clip_path)))


    ## concatenate clips

    final_clip = mp.concatenate_videoclips(clips)

    ## write the clip
    final_clip.write_videofile("final.mp4", fps=24, remove_temp=True)