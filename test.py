from PIL import Image

img_path = '/Users/muskanmall/Desktop/capstone_website/cs_web/static/user_image/sad_girl.jpg'
try:
    # Try opening with PIL to check if the file is accessible and not corrupted
    img = Image.open(img_path)
    img.show()  # This should display the image
except Exception as e:
    print(e)
