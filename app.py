import streamlit as st
from PIL import Image
import imageio
import os
import tempfile

st.set_page_config(page_title="GIF Maker Studio", page_icon="🎥", layout="centered")





st.title("🎥 GIF Maker Studio")
st.write("Create GIFs from images or videos — offline & instant! 🚀")

option = st.radio("Select Mode:", ["Images → GIF", "Video → GIF"])

fps = st.slider("GIF Speed (Frames Per Second)", 1, 30, 10)
width = st.slider("GIF Width (px)", 200, 1000, 500)

if option == "Images → GIF":
    uploaded_files = st.file_uploader(
        "Upload multiple images (JPG/PNG):", type=["jpg", "png"], accept_multiple_files=True
    )

    if st.button("Create GIF") and uploaded_files:
        frames = []

        for file in uploaded_files:
            img = Image.open(file).convert("RGB")
            img = img.resize((width, int(img.height * width / img.width)))
            frames.append(img)

        output_path = "generated.gif"
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=int(1000/fps),
            loop=0
        )

        st.success("🎉 GIF Created Successfully!")
        st.image(output_path)
        st.download_button("Download GIF", open(output_path, "rb"), "my_gif.gif")

elif option == "Video → GIF":
    file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

    if st.button("Convert Video"):
        if file:
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                temp.write(file.read())
                video_path = temp.name

            reader = imageio.get_reader(video_path)
            frames = []

            for i, frame in enumerate(reader):
                img = Image.fromarray(frame)
                img = img.resize((width, int(img.height * width / img.width)))
                frames.append(img)

            output_path = "video.gif"
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=int(1000/fps),
                loop=0
            )

            st.success("🎬 GIF Ready!")
            st.image(output_path)
            st.download_button("Download GIF", open(output_path, "rb"), "video_to_gif.gif")
        else:
            st.error("Upload a video first!")
