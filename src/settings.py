from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "OpenCow2020"
PROJECT_NAME_FULL: str = "OpenCow2020: Visual Identification of Individual Holstein Friesian Cattle via Deep Metric Learning"
HIDE_DATASET = False  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.NCGL_2_0()
APPLICATIONS: List[Union[Industry, Domain, Research]] = [Industry.Livestock()]
CATEGORY: Category = Category.Livestock(extra=Category.Drones())

CV_TASKS: List[CVTask] = [CVTask.ObjectDetection(), CVTask.Identification()]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.ObjectDetection()]

RELEASE_DATE: Optional[str] = "2020-07-03"  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = None

HOMEPAGE_URL: str = "https://data.bris.ac.uk/data/dataset/10m32xl88x2b61zlkkgz3fml17"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 3167443
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/opencows2020"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[
    Union[str, dict]
] = "https://data.bris.ac.uk/datasets/tar/10m32xl88x2b61zlkkgz3fml17.zip"
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = None
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
PAPER: Optional[Union[str, List[str]]] = "https://research-information.bris.ac.uk/en/publications/visual-identification-of-individual-holstein-friesian-cattle-via-"
BLOGPOST: Optional[Union[str, List[str]]] = None
REPOSITORY: Optional[Union[str, List[str]]] = {"GitHub":"https://github.com/CWOA/MetricLearningIdentification"}

CITATION_URL: Optional[str] = "https://doi.org/10.5523/bris.10m32xl88x2b61zlkkgz3fml17"
AUTHORS: Optional[List[str]] = ["William Andrew", "Tilo Burghardt", "Neill Campbell", "Jing Gao"]
AUTHORS_CONTACTS: Optional[List[str]] = ["tb2935@bristol.ac.uk", "andrew.dowsey@bristol.ac.uk"]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = "University of Bristol, UK"
ORGANIZATION_URL: Optional[Union[str, List[str]]] = "https://www.bristol.ac.uk/"

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with string value to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = {
    "detection_and_localisation subsets": ["non-synthetic", "synthetic"],
    "__POSTTEXT__": "Additionally, in *identification-test* and *identification-train* splits information about ***cow_id*** and data ***source*** is provided",
}
TAGS: Optional[List[str]] = None


SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL or PROJECT_NAME,
        "hide_dataset": HIDE_DATASET,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["blog"] = BLOGPOST
    settings["repository"] = REPOSITORY
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["authors_contacts"] = AUTHORS_CONTACTS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
