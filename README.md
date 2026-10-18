# Dockerized Iris model training lab

This lab builds and runs a reproducible Docker image that trains a Random
Forest classifier on scikit-learn's Iris dataset. The training process prints
test accuracy and saves the model to a path that can be mounted from the host.

## Changes made

- Replaced the original Dockerfile with a standard `Dockerfile` based on the
  smaller `python:3.10-slim` image.
- Pinned scikit-learn, joblib, and their numerical/runtime dependencies so
  repeated builds install the same Python package versions.
- Copied and installed the requirements before copying the application, so
  Docker can reuse the dependency-install layer when only the code changes.
- Added a `.dockerignore` to keep local artifacts, archives, and Git metadata
  out of the build context.
- Runs the application as a non-root user in the image.
- Added a configurable `--output` option, test accuracy reporting, and
  persistent model output through a bind mount.

## Prerequisites

- Docker Desktop 4.30 or newer on macOS or Windows, or Docker Engine 25 or
  newer on Linux. Docker must be running before you build or run the lab.
- Git, if you are cloning this repository.
- Internet access for the initial image build to download the base image and
  pinned Python packages. No separate Python installation is needed on the host.

## Get the lab

Clone the repository and move into its directory:

```sh
git clone https://github.com/shivamsinghlive/lab2_docker_mlops-.git
cd lab2_docker_mlops-
docker info
```

`docker info` should show a `Server` section. If it reports that it cannot
connect, start Docker Desktop (macOS/Windows) or the Docker service (Linux)
before continuing.

## Build and run (macOS/Linux)

Run these commands from the repository root:

```sh
docker build -t iris-training:1.0 .
mkdir -p artifacts
docker run --rm \
  --user "$(id -u):$(id -g)" \
  --mount "type=bind,source=$(pwd)/artifacts,target=/artifacts" \
  iris-training:1.0 \
  --output /artifacts/iris_model.joblib
```

The container exits after training. The `--user` option lets the process write
to the host-mounted directory as your account, and the bind mount keeps the
model after the container is removed.

## Build and run (Windows PowerShell)

Run these commands from the repository root:

```powershell
docker build -t iris-training:1.0 .
New-Item -ItemType Directory -Force artifacts | Out-Null
docker run --rm `
  --mount "type=bind,source=$((Resolve-Path artifacts).Path),target=/artifacts" `
  iris-training:1.0 `
  --output /artifacts/iris_model.joblib
```

## Expected result

The run prints output similar to:

```text
Model training successful. Test accuracy: 1.00
Model saved to: /artifacts/iris_model.joblib
```

The trained model will be available on the host at
`artifacts/iris_model.joblib`. The accuracy is expected to be `1.00` with this
fixed train/test split and random seed.

To run the training again after changing code, rebuild the image and rerun the
container:

```sh
docker build -t iris-training:1.0 .
```
