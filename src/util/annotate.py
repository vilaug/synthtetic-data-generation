import json
from datetime import datetime
from pathlib import Path

src_dir = "/workdir"


def get_info(description, version, time_now):
    """
    Gets the information about the dataset
    :param description: description field for the info
    :param version: version field for the info
    :param time_now: current time
    :return: a dict containing the needed information about the dataset
    """
    return dict(description=description,
                version=version, year=time_now.year,
                date_created=f"{time_now.year}/{time_now.month}/{time_now.day}")


def get_image_info(n_images, resolution, time_now):
    """
    Gets the information about the images in the data set
    :param n_images: number of images
    :param resolution: resolution of the images
    :param time_now: current time
    :return: a dict containing the needed information about the images
    """
    image_info = []
    date = f"{time_now.year}/{time_now.month}/{time_now.day}"
    for i in range(n_images):
        image_info.append(
            {
                'id': i,
                'width': resolution[0],
                'height': resolution[1],
                'file_name': f"{i}.jpg",
                'date_captured': date
            }
        )
    return image_info


def get_category_id(object_name, category_dict, name_dict):
    """
    Gets the category id from the object name
    :param object_name: name of the object, should be the material type
    :param category_dict: dictionary of categories
    :param name_dict: dictionary of names as keys and material as value
    :return: an integer of the category or -1 if name was not found
    """
    material = name_dict.get(object_name)
    if material is not None:
        category_id = category_dict['materials'].get(material)

        if category_id is not None:
            return category_id
    return -1


def get_annotation_info(bounding_boxes, category_dict, name_dict):
    """
    Gets the annotations
    :param bounding_boxes: bounding boxes for each image
    :param category_dict: dictionary of categories as specified in the configuration
    :param name_dict: dictionary of names as keys and material as value
    :return: a list containing all the annotations
    """
    annotations = []
    counter = 0
    for i_image, image_bounding_boxes in enumerate(bounding_boxes):
        for i_object, (object_name, object_bounding_box) in enumerate(image_bounding_boxes):
            x, y, width, height = object_bounding_box
            if width + height > 200:
                annotations.append({
                    "id": counter, "image_id": i_image,
                    "category_id": get_category_id(object_name, category_dict, name_dict),
                    "segmentation": [x, y, x + width, y - height, x + width, y, x, y - height],
                    "area": width * height, "bbox": object_bounding_box, "iscrowd": 0,
                })
            counter += 1
    return annotations


def get_category_info(category_dict):
    """
    Gets the category information
    :param category_dict: dictionary of categories
    :return: a list containing all the categories
    """
    categories = []
    for super_category, curr_category_dict in category_dict.items():
        for name, identifier in curr_category_dict.items():
            categories.append({"id": identifier, "name": name, "supercategory": super_category})
    return categories


def write_file(info_configuration, resolution, name, n_images, bounding_boxes):
    """
    Write the file with the needed dataset information
    :param info_configuration: configuration of the info json
    :param resolution: resolution of the images
    :param name: name of the file
    :param n_images: number of images
    :param bounding_boxes: List of len (n_images)
    containing the bounding boxes for each image.
    """
    time_now = datetime.now()
    with open(Path(src_dir + r'/images/' + name + '.json'), 'w') as file:
        json.dump({
            "info": get_info(info_configuration['description'],
                             info_configuration['version'], time_now),
            "images": get_image_info(n_images, resolution, time_now),
            "annotations": get_annotation_info(bounding_boxes, info_configuration['categories'],
                                               info_configuration['names']),
            "categories": get_category_info(info_configuration['categories'])
        },
            file)
