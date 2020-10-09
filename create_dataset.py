import os, glob
import soundfile
import numpy as np
import pandas as pd

# TODO: after downloading the FSL10K dataset, set the correct path below.
FSLD_PATH = os.path.expanduser("~/Downloads/FSL10K")

LOOP_PATHS = glob.glob(FSLD_PATH+"/audio/wav/*.wav")
LOOP_FILENAMES = [os.path.basename(path) for path in LOOP_PATHS]
LOOP_IDS = [filename.split("_")[0] for filename in LOOP_FILENAMES]
PLAN_PATHS = sorted(glob.glob("./generated_plans/*_plan.txt"))
LOOP_FILENAME_DF = pd.DataFrame(data={'path':LOOP_PATHS, 'filename':LOOP_FILENAMES, 'id':LOOP_IDS})
SAMPLE_RATE = 22050

def load_song_data(plan_filename):
    """
    Load a song layout file and return 3 pieces of information:
    - clip id of each loop
    - clip audio arrays
    - layout of loop activations
    """
    plan_data = pd.read_csv(plan_filename, index_col=0)
    n_clips = len(plan_data.index)
    layout = np.array(plan_data.values)
    clip_ids = list(plan_data.index.astype(str).values)
    loop_filenames = [LOOP_FILENAME_DF.loc[LOOP_FILENAME_DF.id==cid, 'path'].iloc[0] for cid in clip_ids]
    clips = [soundfile.read(filename) for filename in loop_filenames]
    return clip_ids, clips, layout

def implement_song_layout(layout, audio_clips):
    """
    Add together audio clips in the pattern dictated by the loop
    layout, assuming:
    - sample rate is 44100
    - each loop is 2 seconds long (1 bar in 4/4 at 120 bpm)
    
    Inputs:
    - layout, a binary array of size (n_clips, n_bars)
        where 1 indicates an activated loop
    - audio_clips, a list of n_clips with each item being a
        tuple (audio_array, sample_rate)
    """
    sample_rate = 44100
    assert np.all([clip[1]==sample_rate for clip in audio_clips])
    if layout.shape[0]>len(audio_clips):
        print("Error! Fewer clip types exist than called for in the layout. We will loop over clip types.")
    loop_length = sample_rate*2
    output_audio = np.zeros(layout.shape[1]*loop_length)
    downbeat_samples = [i*loop_length for i in range(layout.shape[1]+1)]
    for clip_i in range(layout.shape[0]):
        for bar_j in range(layout.shape[1]):
            if layout[clip_i, bar_j]==1:
                valid_length = min(loop_length, len(audio_clips[clip_i][0]))
                output_audio[downbeat_samples[bar_j]:downbeat_samples[bar_j]+valid_length] += audio_clips[clip_i][0][:valid_length]
    return output_audio

if __name__ == "__main__":
    """
    Creates all the clips and saves as wav files
    """
    for plan_file_path in PLAN_PATHS:
        full_song_filename, _ = os.path.splitext(plan_file_path)
        rendered_filename = full_song_filename + ".wav"
        clip_ids, audio_clips, layout = load_song_data(plan_file_path)
        song_audio = implement_song_layout(layout, audio_clips)
        # print(full_song_filename)
        soundfile.write(rendered_filename, song_audio, 44100)
