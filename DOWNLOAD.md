Dataset **OpenCow2020** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogInMzOi8vc3VwZXJ2aXNlbHktZGF0YXNldHMvMTg3Nl9PcGVuQ293MjAyMC9vcGVuY293MjAyMC1EYXRhc2V0TmluamEudGFyIiwgInNpZyI6ICI0WEZmblFEMDBPVm5yNWoyREVSbE1TMkxKeTFpVHg2bThUWHdDc2dSK1NnPSJ9?response-content-disposition=attachment%3B%20filename%3D%22opencow2020-DatasetNinja.tar%22)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='OpenCow2020', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://data.bris.ac.uk/datasets/tar/10m32xl88x2b61zlkkgz3fml17.zip).