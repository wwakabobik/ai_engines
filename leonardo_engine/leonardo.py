import json
import logging
import os

import asyncio
import aiofiles
import aiohttp


class Leonardo:
    """
    This class is for managing and interacting with Leonardo.ai service.

    Parameters:
    auth_token (str): Auth Bearer token. Required.
    logger (logging.Logger, optional): default logger. Default is None.
    """

    def __init__(self, auth_token: str, logger: logging.Logger = None):
        """
        Constructs all the necessary attributes for the Leonardo object.

        :param auth_token: Auth Bearer token. Required.
        :param logger: default logger. Default is None.
        """
        self.___session = aiohttp.ClientSession(headers={"Authorization": f"Bearer {auth_token}"})
        self.___logger = logger
        self.___get_headers = {"content-type": "application/json"}
        self.___post_headers = {"accept": "application/json", "content-type": "application/json"}

    async def get_user_info(self):
        """
        This endpoint will return your user information, including your user ID.
        """
        url = "https://cloud.leonardo.ai/api/rest/v1/me"
        async with self.___session.get(
            url, headers=self.___session.headers.copy().update(self.___get_headers)
        ) as response:
            return await response.json()

    async def post_generations(
        self,
        prompt: str,
        negative_prompt: str = None,
        model_id: str = None,
        sd_version: str = None,
        num_images: int = 4,
        width: int = 512,
        height: int = 512,
        num_inference_steps: int = None,
        guidance_scale: int = None,
        init_generation_image_id: str = None,
        init_image_id: str = None,
        init_strength: float = None,
        scheduler: str = None,
        preset_style: str = None,
        tiling: bool = False,
        public: bool = False,
        prompt_magic: bool = True,
        control_net: bool = None,
        control_net_type: str = None,
    ):
        """
        This endpoint will generate images.

        :param prompt: The prompt used to generate images.
        :param negative_prompt: The negative prompt used for the image generation.
        :param model_id: The model ID used for the image generation.
        :param sd_version: The base version of stable diffusion to use if not using a custom model.
        :param num_images: The number of images to generate. Default is 4.
        :param width: The width of the images. Default is 512px.
        :param height: The height of the images. Default is 512px.
        :param num_inference_steps: The number of inference steps to use for the generation.
        :param guidance_scale: How strongly the generation should reflect the prompt.
        :param init_generation_image_id: The ID of an existing image to use in image2image.
        :param init_image_id: The ID of an Init Image to use in image2image.
        :param init_strength: How strongly the generated images should reflect the original image in image2image.
        :param scheduler: The scheduler to generate images with.
        :param preset_style: The style to generate images with.
        :param tiling: Whether the generated images should tile on all axis. Default is False.
        :param public: Whether the generated images should show in the community feed. Default is False.
        :param prompt_magic: Enable to use Prompt Magic. Default is True.
        :param control_net: Enable to use ControlNet. Requires an init image to be provided.
                            Requires a model based on SD v1.5
        :param control_net_type: The type of ControlNet to use.
        """
        url = "https://cloud.leonardo.ai/api/rest/v1/generations"
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "modelId": model_id,
            "sd_version": sd_version,
            "num_images": num_images,
            "width": width,
            "height": height,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "init_generation_image_id": init_generation_image_id,
            "init_image_id": init_image_id,
            "init_strength": init_strength,
            "scheduler": scheduler,
            "presetStyle": preset_style,
            "tiling": tiling,
            "public": public,
            "promptMagic": prompt_magic,
            "controlNet": control_net,
            "controlNetType": control_net_type,
        }
        async with self.___session.post(
            url, json=payload, headers=self.___session.headers.copy().update(self.___post_headers)
        ) as response:
            return await response.json()

    async def get_single_generation(self, generation_id: str):
        """
        This endpoint will provide information about a specific generation.

        :param generation_id: The ID of the generation to return.
        """
        url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
        async with self.___session.get(
            url, headers=self.___session.headers.copy().update(self.___get_headers)
        ) as response:
            return await response.json()

    async def delete_single_generation(self, generation_id: str):
        """
        This endpoint deletes a specific generation.

        :param generation_id: The ID of the generation to delete.
        """
        url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
        async with self.___session.delete(
            url, headers=self.___session.headers.copy().update(self.___get_headers)
        ) as response:
            return await response.json()

    async def get_generations_by_user(self, user_id: str, offset: int = 0, limit: int = 10):
        """
        This endpoint returns all generations by a specific user.

        :param user_id: The ID of the user.
        :param offset: The offset for pagination.
        :param limit: The limit for pagination.
        """
        url = f"https://cloud.leonardo.ai/api/rest/v1/generations/user/{user_id}"
        params = {"offset": offset, "limit": limit}
        async with self.___session.get(
            url, params=params, headers=self.___session.headers.copy().update(self.___get_headers)
        ) as response:
            return await response.json()

    async def upload_init_image(self, file_path: str):
        """
        This endpoint returns presigned details to upload an init image to S3.

        :param file_path: The path to the image file.
        """
        valid_extensions = ["png", "jpg", "jpeg", "webp"]
        extension = os.path.splitext(file_path)[1].strip(".")
        if extension not in valid_extensions:
            raise ValueError(f"Invalid file extension. Must be one of {valid_extensions}")

        url = "https://cloud.leonardo.ai/api/rest/v1/init-image"
        payload = {"extension": extension}
        async with self.___session.post(
            url, json=payload, headers=self.___session.headers.copy().update(self.___post_headers)
        ) as response:
            data = await response.json()

        upload_url = data["uploadInitImage"]["url"]
        fields = json.loads(data["uploadInitImage"]["fields"])

        async with aiofiles.open(file_path, "rb") as f:
            file_data = await f.read()

        fields.update({"file": file_data})

        async with self.___session.post(
            upload_url, data=fields, headers=self.___session.headers.copy().update(self.___post_headers)
        ) as response:
            return await response.text()

    async def get_single_init_image(self, image_id: str):
        """
        This endpoint will return a single init image.

        :param image_id: The ID of the init image to return.
        """
        url = f"https://cloud.leonardo.ai/api/rest/v1/init-image/{image_id}"
        async with self.___session.get(
            url, headers=self.___session.headers.copy().update(self.___get_headers)
        ) as response:
            return await response.json()

    async def delete_init_image(self, image_id: str):
        """
        This endpoint deletes an init image.

        :param image_id: The ID of the init image to delete.
        """
        url = f"https://cloud.leonardo.ai/api/rest/v1/init-image/{image_id}"
        async with self.___session.delete(
            url, headers=self.___session.headers.copy().update(self.___get_headers)
        ) as response:
            return await response.json()

    async def create_upscale(self, image_id: str):
        """
        This endpoint will create an upscale for the provided image ID.

        :param image_id: The ID of the image to upscale.
        """
        url = "https://cloud.leonardo.ai/api/rest/v1/variations/upscale"
        payload = {"id": image_id}
        async with self.___session.post(
            url, json=payload, headers=self.___session.headers.copy().update(self.___post_headers)
        ) as response:
            return await response.json()

    async def get_variation_by_id(self, generation_id: str):
        """
        This endpoint will get the variation by ID.

        :param generation_id: The ID of the variation to get.
        """
        url = f"https://cloud.leonardo.ai/api/rest/v1/variations/{generation_id}"
        async with self.___session.get(
            url, headers=self.___session.headers.copy().update(self.___get_headers)
        ) as response:
            return await response.json()

    async def create_dataset(self, name: str, description: str = None):
        """
        This endpoint creates a new dataset.

        :param name: The name of the dataset.
        :param description: A description for the dataset.
        """
        url = "https://cloud.leonardo.ai/api/rest/v1/datasets"
        payload = {"name": name, "description": description}
        async with self.___session.post(
            url, json=payload, headers=self.___session.headers.copy().update(self.___post_headers)
        ) as response:
            return await response.json()

    async def get_dataset_by_id(self, dataset_id: str):
        """
        This endpoint gets the specific dataset.

        :param dataset_id: The ID of the dataset to return.
        """
        url = f"https://cloud.leonardo.ai/api/rest/v1/datasets/{dataset_id}"
        async with self.___session.get(
            url, headers=self.___session.headers.copy().update(self.___get_headers)
        ) as response:
            return await response.json()

    async def delete_dataset_by_id(self, id: str):
        """
        This endpoint deletes the specific dataset.

        :param id: The ID of the dataset to delete.
        """
        url = f"https://cloud.leonardo.ai/api/rest/v1/datasets/{id}"
        async with self.___session.delete(
            url, headers=self.___session.headers.copy().update(self.___get_headers)
        ) as response:
            return await response.json()

    async def upload_dataset_image(self, dataset_id: str, file_path: str):
        """
        This endpoint returns presigned details to upload a dataset image to S3.

        :param dataset_id: The ID of the dataset to which the image will be uploaded.
        :param file_path: The path to the image file.
        """
        valid_extensions = ["png", "jpg", "jpeg", "webp"]
        extension = os.path.splitext(file_path)[1].strip(".")
        if extension not in valid_extensions:
            raise ValueError(f"Invalid file extension. Must be one of {valid_extensions}")

        url = f"https://cloud.leonardo.ai/api/rest/v1/datasets/{dataset_id}/upload"
        payload = {"extension": extension}
        async with self.___session.post(
            url, json=payload, headers=self.___session.headers.copy().update(self.___post_headers)
        ) as response:
            data = await response.json()

        upload_url = data["uploadDatasetImage"]["url"]
        fields = json.loads(data["uploadDatasetImage"]["fields"])

        async with aiofiles.open(file_path, "rb") as f:
            file_data = await f.read()

        fields.update({"file": file_data})

        async with self.___session.post(
            upload_url, data=fields, headers=self.___session.headers.copy().update(self.___post_headers)
        ) as response:
            return await response.text()

    async def upload_generated_image_to_dataset(self, dataset_id: str, generated_image_id: str):
        """
        This endpoint will upload a previously generated image to the dataset.

        :param dataset_id: The ID of the dataset to upload the image to.
        :param generated_image_id: The ID of the image to upload to the dataset.
        """
        url = f"https://cloud.leonardo.ai/api/rest/v1/datasets/{dataset_id}/upload/gen"
        payload = {"generatedImageId": generated_image_id}
        async with self.___session.post(
            url, json=payload, headers=self.___session.headers.copy().update(self.___post_headers)
        ) as response:
            return await response.json()

    async def train_custom_model(
        self,
        name: str,
        dataset_id: str,
        instance_prompt: str,
        description: str = None,
        model_type: str = "GENERAL",
        nsfw: bool = False,
        resolution: int = 512,
        sd_version: str = None,
        strength: str = "MEDIUM",
    ):
        """
        This endpoint will train a new custom model.

        :param name: The name of the model.
        :param description: The description of the model.
        :param dataset_id: The ID of the dataset to train the model on.
        :param instance_prompt: The instance prompt to use during training.
        :param model_type: The category the most accurately reflects the model.
        :param nsfw: whether or not the model is NSFW.
        :param resolution: The resolution for training. Must be 512 or 768.
        :param sd_version: The base version of stable diffusion to use if not using a custom model.
        :param strength: When training using the PIXEL_ART model type, this influences the training strength.
        """
        url = "https://cloud.leonardo.ai/api/rest/v1/models"
        payload = {
            "name": name,
            "description": description,
            "datasetId": dataset_id,
            "instance_prompt": instance_prompt,
            "modelType": model_type,
            "nsfw": nsfw,
            "resolution": resolution,
            "sd_Version": sd_version,
            "strength": strength,
        }
        async with self.___session.post(
            url, json=payload, headers=self.___session.headers.copy().update(self.___post_headers)
        ) as response:
            return await response.json()

    async def get_custom_model_by_id(self, model_id: str):
        """
        This endpoint gets the specific custom model.

        :param model_id: The ID of the custom model to return.
        """
        url = f"https://cloud.leonardo.ai/api/rest/v1/models/{model_id}"
        async with self.___session.get(
            url, headers=self.___session.headers.copy().update(self.___get_headers)
        ) as response:
            return await response.json()

    async def delete_custom_model_by_id(self, model_id: str):
        """
        This endpoint will delete a specific custom model.

        :param model_id: The ID of the model to delete.
        """
        url = f"https://cloud.leonardo.ai/api/rest/v1/models/{model_id}"
        async with self.___session.delete(
            url, headers=self.___session.headers.copy().update(self.___get_headers)
        ) as response:
            return await response.json()

    async def wait_for_image_generation(self, generation_id, image_index=None, poll_interval=5):
        """
        This method waits for the completion of image generation.

        :param generation_id: The ID of the generation to check.
        :param image_index: (Optional) The index of the specific image to wait for. If None, waits for all images to complete.
        :param poll_interval: (Optional) The time interval in seconds between each check. Default is 5 seconds.

        :raises IndexError: If an invalid image_index is provided.

        :return: The completed image(s) once generation is complete.
        """
        while True:
            response = await self.get_single_generation(generation_id)
            generation = response.get('generations_by_pk', {})
            images = generation.get('generated_images', [])

            if image_index is not None:
                if image_index >= len(images):
                    raise IndexError("Incorrect image index")
                if images[image_index].get('status') == 'COMPLETE':
                    return images[image_index]
            else:
                if all(image.get('status') == 'COMPLETE' for image in images):
                    return images

            await asyncio.sleep(poll_interval)