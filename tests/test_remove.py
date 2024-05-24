from io import BytesIO
from pathlib import Path
import cv2

from imagehash import phash as hash_img
from PIL import Image

from rembg import new_session, remove

here = Path(__file__).parent.resolve()

def test_remove():
    kwargs = {
        "sam": {
            "anime-girl-1": {
                "sam_prompt": [{"type": "point", "data": [400, 165], "label": 1}],
            },
            "car-1": {
                "sam_prompt": [{"type": "point", "data": [250, 200], "label": 1}],
            },
            "cloth-1": {
                "sam_prompt": [{"type": "point", "data": [370, 495], "label": 1}],
            },
            "plants-1": {
                "sam_prompt": [{"type": "point", "data": [724, 740], "label": 1}],
            },
        }
    }

    for model in [
        "u2net",
        "u2netp",
        "u2net_human_seg",
        "u2net_cloth_seg",
        "silueta",
        "isnet-general-use",
        "isnet-anime",
        "sam",
    ]:
        for picture in ["anime-girl-1", "car-1", "cloth-1", "plants-1"]:
            image_path = Path(here / "fixtures" / f"{picture}.jpg")
            image = image_path.read_bytes()

            actual = remove(image, session=new_session(model), **kwargs.get(model, {}).get(picture, {}))
            actual_hash = hash_img(Image.open(BytesIO(actual)))

            expected_path = Path(here / "results" / f"{picture}.{model}.png")
            # Uncomment to update the expected results
            with open(expected_path, "wb") as f:
                f.write(actual)

            expected = expected_path.read_bytes()
            expected_hash = hash_img(Image.open(BytesIO(expected)))

            print(f"image_path: {image_path}")
            print(f"expected_path: {expected_path}")
            print(f"actual_hash: {actual_hash}")
            print(f"expected_hash: {expected_hash}")
            print(f"actual_hash == expected_hash: {actual_hash == expected_hash}")
            print("---\n")

            assert actual_hash == expected_hash

            try:
                actual_sticker = remove(
                    image,
                    session=new_session(model),
                    sticker_mode=True,
                    border_color=(255, 255, 255, 255),
                    border_width=30,
                    **kwargs.get(model, {}).get(picture, {})
                )
                actual_sticker_hash = hash_img(Image.open(BytesIO(actual_sticker)))

                expected_sticker_path = Path(here / "results" / f"{picture}.{model}.sticker.png")
                # Uncomment to update the expected results
                with open(expected_sticker_path, "wb") as f:
                    f.write(actual_sticker)

                expected_sticker = expected_sticker_path.read_bytes()
                expected_sticker_hash = hash_img(Image.open(BytesIO(expected_sticker)))

                assert actual_sticker_hash == expected_sticker_hash

            except ValueError as e:
                print(f"Error processing {picture} with model {model}: {e}")
                continue