import os
from PIL import Image

def split_gif_into_frames(gif_path):
    """
    Splits a GIF into its frames and saves each as a PNG in a folder named after the GIF.

    Parameters
    ----------
    gif_path : str
        Path to the input GIF file.
    """
    base_name = os.path.splitext(os.path.basename(gif_path))[0]
    output_dir = os.path.join(os.path.dirname(gif_path), base_name)
    os.makedirs(output_dir, exist_ok=True)

    with Image.open(gif_path) as im:
        frame = 0
        while True:
            frame_path = os.path.join(output_dir, f"frame_{frame:04d}.png")
            im.convert("RGBA").save(frame_path)
            frame += 1
            try:
                im.seek(frame)
            except EOFError:
                break
    print(f"Saved {frame} frames to {output_dir}")

#split_gif_into_fr  ames("animation_data/animation.gif")
split_gif_into_frames("sphere_final.gif")