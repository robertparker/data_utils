def get_image_from_url(url):
    from PIL import Image
    import requests
    from io import BytesIO

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


def get_imagekit_urls(limit=100):
    from imagekitio import ImageKit
    import json

    imagekit = ImageKit(
        private_key=os.environ["IMAGEKIT_PRIVATE_KEY"],
        public_key=os.environ["IMAGEKIT_PUBLIC_KEY"],
        url_endpoint=os.environ["IMAGEKIT_URL_ENDPOINT"],
    )

    print(json.dumps(imagekit.list_files({"limit": limit})))


if __name__ == "__main__":
    get_imagekit_urls()
