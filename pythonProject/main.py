import os
import time

from PIL import Image
import streamlit as st


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


path_img = "./"


def compress_img(image_name, new_size_ratio=0.9, quality=90, width=None, height=None, to_jpg=True):
    # load the image to memory
    img = Image.open(image_name)
    # st.write the original image shape
    st.write("[*] Image shape:", img.size)
    # get the original image size in bytes
    image_size = os.path.getsize(image_name)
    # st.write the size before compression/resizing
    st.write("[*] Size before compression:", get_size_format(image_size))
    if new_size_ratio < 1.0:
        # if resizing ratio is below 1.0, then multiply width & height with this ratio to reduce image size
        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)),
                         Image.Resampling.LANCZOS)
        # st.write new image shape
        st.write("[+] New Image shape:", img.size)
    elif width and height:
        # if width and height are set, resize with them instead
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        # st.write new image shape
        st.write("[+] New Image shape:", img.size)
    # split the filename and extension
    filename, ext = os.path.splitext(image_name)
    # make new filename appending _compressed to the original file name
    if to_jpg:
        # change the extension to JPEG
        new_filename = f"{filename}_compressed.jpg"
    else:
        # retain the same extension of the original image
        new_filename = f"{filename}_compressed{ext}"
    try:
        # save the image with the corresponding quality and optimize set to True
        img.save(new_filename, quality=quality, optimize=True)
    except OSError:
        # convert the image to RGB mode first
        img = img.convert("RGB")
        # save the image with the corresponding quality and optimize set to True
        img.save(new_filename, quality=quality, optimize=True)
    st.write("[+] New file saved:", new_filename)
    # get the new image size in bytes
    new_image_size = os.path.getsize(new_filename)
    # st.write the new size in a good format
    st.write("[+] Size after compression:", get_size_format(new_image_size))
    # calculate the saving bytes
    saving_diff = new_image_size - image_size
    # st.write the saving percentageconda activate jpeg
    st.image(path_img + "/" + new_filename, caption='Ảnh sau khi nén')
    download_img(new_filename)

# download
def download_img(img_file):
    with open(path_img + "/" + img_file, "rb") as file:
        st.download_button(
            label="Download image: " + img_file,
            data=file,
            file_name="download.jpg",
            mime="image/jpeg",
        )
    return


# Title
new_title = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">Compress image JPEG web</p>'
st.markdown(new_title, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Ảnh PNG")
with st.spinner("processing..."):
    time.sleep(1)
    if uploaded_file is not None:
        img = path_img + "/" + uploaded_file.name
        st.image(img, caption='Ảnh gốc')
        # If new_size_ratio is set below 1.0, then resizing is necessary. This number ranges from 0 to 1 and is
        # multiplied by the width and height of the original image to come up with a lower resolution image.This is a
        # suitable parameter if you want to reduce the image size further.You can also set it to 0.95 or 0.9 to
        # reduce the image size with minimal changes to the resolution.
        resize_ratio = st.number_input(value=1.0, min_value=0.0, max_value=1.0, label='Resize ratio(0-1)', step=0.1)
        # The image quality, on a scale from 1 (worst) to 95 (best). The default is 75.
        # Values above 95 should be avoided; 100 disables portions of the JPEG compression algorithm,
        # and results in large files with hardly any gain in image quality.

        quality = st.number_input(value=90, min_value=1, max_value=100, label='Quality (0-100)', step=1)
        st.write("=" * 50)
        st.write("[*] Image Path:", uploaded_file.name)
        st.write("[*] To JPEG:", True)
        st.write("[*] Quality:", quality)
        st.write("[*] Resize ratio:", resize_ratio)

        if st.button("Nén ảnh theo chuẩn JPEG"):
            compress_img(image_name=img, new_size_ratio=resize_ratio, quality=quality)
