# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.158.0/containers/python-3-miniconda/.devcontainer/base.Dockerfile

FROM mcr.microsoft.com/vscode/devcontainers/miniconda:0-3

# Add bash
# RUN apk add --no-cache bash

# Add PATH
ENV PATH /opt/conda/bin/:$PATH

# Copy environment.yml + requirements.dev.txt
COPY docs/environment.doc.yml requirements.dev.txt /workspaces/ensemble/

RUN if [ -f "/workspaces/ensemble/environment.doc.yml" ]; then /opt/conda/bin/conda env create -f /workspaces/ensemble/environment.doc.yml; fi

# Activate + dev-tools
RUN /bin/bash -c conda activate ensemble\
    && pip install -r /workspaces/ensemble/requirements.dev.txt\
    && rm -rf /workspaces/ensemble/

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends build-essential