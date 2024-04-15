import imageio.v3 as iio
import os, sys
import numpy as np
from pygifsicle import optimize

class TargetFormat(object):
    GIF = ".gif"
    MP4 = ".mp4"
    AVI = ".avi"

def convertFile(input_path, targetFormat):
    """Reference: http://imageio.readthedocs.io/en/latest/examples.html#convert-a-movie"""
    output_path = os.path.splitext(input_path)[0] + targetFormat
    print("converting\r\n\t{0}\r\nto\r\n\t{1}".format(input_path, output_path))

    data = iio.imread(input_path)
    
    metadata = iio.immeta(input_path)
    fps = metadata.get('fps', 30)
    target_fps = 10
    duration = metadata.get('duration', len(data)/fps)
    
    print(f"fps: {fps}, duration: {duration}")

    frames = []
    FADE_DURATION = 0.75
    # Fade in the first frame
    first_frame = data[0]
    for i in range(int(fps*FADE_DURATION)):
        # Fade from black
        faded_frame = first_frame * 0.9 * (i/(fps*FADE_DURATION))
        faded_frame = faded_frame.astype(np.uint8)
        frames.append(faded_frame)
    
    for i, im in enumerate(data):
        sys.stdout.write("\rFrame {0}".format(i))
        sys.stdout.flush()
        frames.append(im)
    
    # Repeat and fade the last frame
    last_frame = frames[-1]
    for i in range(int(fps*FADE_DURATION)):
        # Fade to black
        faded_frame = last_frame * (1 - 0.9 * i/(fps*FADE_DURATION))
        faded_frame = faded_frame.astype(np.uint8)
        frames.append(faded_frame)
    
    # Skip frames to reduce the size of the gif
    skip_frames = int(fps/target_fps)
    frames = frames[::skip_frames]
    
    print("\r\nWriting...")
    iio.imwrite(output_path, frames, format='GIF', duration=duration, fps=target_fps, loop=0)
    print("\r\nOptimizing...")
    optimize(output_path)

    # writer = imageio.get_writer(output_path, fps=fps, format='GIF')
    # for i,im in enumerate(reader):
    #     sys.stdout.write("\rFrame {0}".format(i))
    #     sys.stdout.flush()
    #     writer.append_data(im)

    # print("\r\nFinalizing...")
    # writer.close()
    
    # Open the newly created file
    
    print("Done.")

# Read the command line arguments
if __name__ == "__main__":
    # Check if the input path is provided
    if len(sys.argv) != 2:
        print("Usage: video-to-gif <input_path>")
        sys.exit(1)
    targetFormat = TargetFormat.GIF

    input_path = sys.argv[1]
    is_dir = os.path.isdir(input_path)
    # Convert all files in directory, otherwise convert the file
    if is_dir:
        for file in os.listdir(input_path):
            if file.endswith(".mp4"):
                convertFile(os.path.join(input_path, file), targetFormat)
    else:
        convertFile(input_path, targetFormat)