FROM craigwillis/cs598-hw5-base:v1
LABEL cs598_fdc="jihyung3@illinois.edu"

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    graphviz \ && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \    pandas \    rdflib \    lxml \    prov \    graphviz

WORKDIR /work
