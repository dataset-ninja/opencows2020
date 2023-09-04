# https://data.bris.ac.uk/data/dataset/10m32xl88x2b61zlkkgz3fml17

import glob
import os
import xml.etree.ElementTree as ET

import numpy as np
import supervisely as sly
from dotenv import load_dotenv
from supervisely.io.fs import (
    dir_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from supervisely.io.json import load_json_file
from tqdm import tqdm

import src.settings as s
from dataset_tools.convert import unpack_if_archive


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "Open cows 2020"
    dataset_path = "/mnt/d/datasetninja-raw/opencows2020/10m32xl88x2b61zlkkgz3fml17"
    batch_size = 30
    images_ext = ".jpg"
    ann_ext = ".xml"

    def create_ann(image_path):
        labels = []
        tags = []

        if subfolder == "detection_and_localisation":
            image_name_number = int(get_file_name(image_path))
            if image_name_number > 3707:
                synthetic = sly.Tag(tag_synthetic)
            else:
                synthetic = sly.Tag(tag_non_synthetic)
            tags.append(synthetic)

            ann_path = os.path.join(bboxes_path, get_file_name(image_path) + ann_ext)

            tree = ET.parse(ann_path)
            root = tree.getroot()
            img_height = int(root.find(".//height").text)
            img_width = int(root.find(".//width").text)
            objects_content = root.findall(".//object")
            for obj_data in objects_content:
                bndbox = obj_data.find(".//bndbox")
                top = int(bndbox.find(".//ymin").text)
                left = int(bndbox.find(".//xmin").text)
                bottom = int(bndbox.find(".//ymax").text)
                right = int(bndbox.find(".//xmax").text)

                rectangle = sly.Rectangle(top=top, left=left, bottom=bottom, right=right)
                label = sly.Label(rectangle, obj_class)
                labels.append(label)

        else:
            image_np = sly.imaging.image.read(image_path)[:, :, 0]
            img_height = image_np.shape[0]
            img_width = image_np.shape[1]

            id_value = int(image_path.split("/")[-2])
            tag_id = sly.Tag(tag_cow_id, value=id_value)
            tags.append(tag_id)

            if id_value < 18:
                source_value = "Andrew (2019) et al. https://doi.org/10.1109/IROS40897.2019.8968555"
            elif id_value > 39:
                source_value = "Andrew (2017) et al. https://doi.org/10.1109/ICCVW.2017.336"
            else:
                source_value = "Andrew (2016) et al. https://doi.org/10.1109/ICIP.2016.7532404"

            source = sly.Tag(tag_source, value=source_value)
            tags.append(source)

        return sly.Annotation(img_size=(img_height, img_width), labels=labels, img_tags=tags)

    obj_class = sly.ObjClass("cow", sly.Rectangle)

    tag_synthetic = sly.TagMeta("synthetic", sly.TagValueType.NONE)
    tag_non_synthetic = sly.TagMeta("non_synthetic", sly.TagValueType.NONE)
    tag_cow_id = sly.TagMeta("cow_id", sly.TagValueType.ANY_NUMBER)
    tag_source = sly.TagMeta("source", sly.TagValueType.ANY_STRING)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[obj_class],
        tag_metas=[tag_cow_id, tag_synthetic, tag_non_synthetic, tag_source],
    )
    api.project.update_meta(project.id, meta.to_json())

    for subfolder in os.listdir(dataset_path):
        data_path = os.path.join(dataset_path, subfolder)
        if dir_exists(data_path):
            images_path = os.path.join(data_path, "images")

            if subfolder == "detection_and_localisation":
                ds_name = subfolder
                dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)
                bboxes_path = os.path.join(data_path, "labels-xml")

                images_names = [
                    im_name
                    for im_name in os.listdir(images_path)
                    if get_file_ext(im_name) == images_ext
                ]

                progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

                for img_names_batch in sly.batched(images_names, batch_size=batch_size):
                    images_pathes_batch = [
                        os.path.join(images_path, image_name) for image_name in img_names_batch
                    ]

                    img_infos = api.image.upload_paths(
                        dataset.id, img_names_batch, images_pathes_batch
                    )
                    img_ids = [im_info.id for im_info in img_infos]

                    anns = [create_ann(image_path) for image_path in images_pathes_batch]
                    api.annotation.upload_anns(img_ids, anns)

                    progress.iters_done_report(len(img_names_batch))

            else:
                for split_folder in os.listdir(images_path):
                    curr_images_path = os.path.join(images_path, split_folder)
                    if dir_exists(curr_images_path):
                        suffix = split_folder
                        ds_name = subfolder + "-" + suffix
                        dataset = api.dataset.create(
                            project.id, ds_name, change_name_if_conflict=True
                        )

                        images_pathes = glob.glob(curr_images_path + "/*/*.jpg")

                        progress = sly.Progress(
                            "Create dataset {}".format(ds_name), len(images_pathes)
                        )

                        for images_pathes_batch in sly.batched(
                            images_pathes, batch_size=batch_size
                        ):
                            img_names_batch = [
                                image_path.split("/")[-2] + "_" + get_file_name_with_ext(image_path)
                                for image_path in images_pathes_batch
                            ]

                            img_infos = api.image.upload_paths(
                                dataset.id, img_names_batch, images_pathes_batch
                            )
                            img_ids = [im_info.id for im_info in img_infos]

                            anns = [create_ann(image_path) for image_path in images_pathes_batch]
                            api.annotation.upload_anns(img_ids, anns)

                            progress.iters_done_report(len(img_names_batch))
    return project
