import imageio
import os, sys

class TargetFormat(object):
    GIF = ".gif"
    MP4 = ".mp4"
    AVI = ".avi"

def convertFile(input_path, targetFormat):
    """Reference: http://imageio.readthedocs.io/en/latest/examples.html#convert-a-movie"""
    output_path = os.path.splitext(input_path)[0] + targetFormat
    print("converting\r\n\t{0}\r\nto\r\n\t{1}".format(input_path, output_path))

    reader = imageio.get_reader(input_path)
    fps = reader.get_meta_data()['fps']

    writer = imageio.get_writer(output_path, fps=fps)
    for i,im in enumerate(reader):
        sys.stdout.write("\rFrame {0}".format(i))
        sys.stdout.flush()
        writer.append_data(im)
    print("\r\nFinalizing...")
    writer.close()
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