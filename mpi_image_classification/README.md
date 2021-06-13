Image classification distributed training pipeline
=========================================
This is a sample to demonstrate distributed training in azure machine learning. In this pipeline, we use designer built-in modules to do image preprocessing on cpu nodes, and a mpi custom module on distributed gpu nodes.

Pipeline graph
-----------------------------
![Pipeline graph](./image_classification_pipeline.png)

Dataset
-----------------------------
This smaller imagenet dataset is a subset of the official one, saved in \\pengwa01\shares\training\autoresize\imagenet\2012

- training dataset contains 9100 images (7 categories * 1300 images per category)
- validation dataset contains 350 images (7 categories * 50 images per category)

Need to use zip file here to avoid perf issue in mounting file dataset with many sub-folders.

Results
-----------------------------
See logs in [this pipeline run](https://ml.azure.com/experiments/id/ee38a17a-5dc2-4ceb-ad52-c02b64de3762/runs/e58ad610-bb53-436a-a8d8-9b5116d5c888?wsid=/subscriptions/4aaa645c-5ae2-4ae9-a17a-84b9023bc56a/resourcegroups/itp-pilot-ResGrp/workspaces/itp-pilot&tid=72f988bf-86f1-41af-91ab-2d7cd011db47).
