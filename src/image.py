from typing import Optional
from PIL import Image
from imagekitio import ImageKit
import requests
from io import BytesIO
import json
import os


def get_image_from_url(url: str) -> Image:
    """returns an Image object from a given url"""
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


def get_imagekit_urls(limit: Optional[int] = 100) -> None:
    """gets imagekit urls for a given set of credentials"""
    imagekit = ImageKit(
        private_key=os.environ["IMAGEKIT_PRIVATE_KEY"],
        public_key=os.environ["IMAGEKIT_PUBLIC_KEY"],
        url_endpoint=os.environ["IMAGEKIT_URL_ENDPOINT"],
    )

    print(json.dumps(imagekit.list_files({"limit": limit})))


if __name__ == "__main__":
    get_imagekit_urls()
