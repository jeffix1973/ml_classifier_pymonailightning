# ml_classifier_pymonailightning
DICOM image classifier using Pytorch MONAI

# Env
conda env create -f environment.yml

# Tensorboard
tensorboard --logdir=logs/fit

# Train / test loop (--mode train, test or both)
python main.py --mode both --json_path <path_to_model-ax-sag-or-cor_json_file>
> Ex: python main.py --mode both --json_path /data/origin/AI/datasets/sidviewer/rh8-dev02-0.0.0_monai/model_params_ax.json

# Prepare Docker
python prepare_docker.py --json_path <path_to_common_json_file>

# Docker
## Docker command to build base cnn_monai_1.3_inference image
>$ docker build -t cnn_monai_1.3_inference -f Dockerfile_base_image .

## Docker command to build the model image / the base image
>$ docker build -t mr_bp_monai_test -f Dockerfile_app .

## Run image
>$ docker run --rm -p 5000:5000 -v /data/BDs/:/dicom --name mr_bp_monai_test mr_bp_monai_test

# Testing locally with Curl
## AX Model
```
curl -X POST http://localhost:5000/ax -H "Content-Type: application/json" -d '{"filepath": "/data/BDs/TELEDIAG_HEAD/6/2.16.840.1.113669.632.20.785037807.537038478.10000252444/1.3.46.670589.11.45070.5.0.8276.2021122409065105043/1.3.46.670589.11.45070.5.0.8276.2021122409083947122.dcm"}'
```

## SAG Model
```
curl -X POST http://localhost:5000/sag -H "Content-Type: application/json" -d '{"filepath": "/data/BDs/TELEDIAG_HEAD/6/2.16.840.1.113669.632.20.785037807.537038478.10000252601/1.2.840.113619.2.311.259076417166205118018582012424746024474/1.2.840.113619.2.311.322411204475891378704579555514521296708.dcm"}'
```

## COR Model
```
curl -X POST http://localhost:5000/cor -H "Content-Type: application/json" -d '{"filepath": "/data/BDs/TELEDIAG_HEAD/6/2.16.840.1.113669.632.20.785037807.537038478.10000251622/1.3.46.670589.11.45070.5.0.8276.2021122312103627986/1.3.46.670589.11.45070.5.0.8276.2021122312142022035.dcm"}'
```

## Typical response
```
{
  "ModelName": "models/model_ax",
  "Predictions": {
    "ModelOutputClasses": [
      "HEAD.ZONE_BRAIN",
      "HEAD.ZONE_EYES",
      "HEAD.ZONE_NOSE",
      "HEAD.ZONE_MOUTH"
    ],
    "PredictedClass": "HEAD.ZONE_EYES"
  },
  "SOPInstanceUID": "1.3.46.670589.11.45070.5.0.8276.2021122409083947122",
  "Scores": [
    0.022186066955327988,
    0.966820240020752,
    0.010952775366604328,
    4.089216599822976e-05
  ],
  "SeriesInstanceUID": "1.3.46.670589.11.45070.5.0.8276.2021122409065105043",
  "StudyInstanceUID": "2.16.840.1.113669.632.20.785037807.537038478.10000252444"
}
```


