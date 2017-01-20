# Innervate

Innervate is a chaos engine for simulating user interactions with
services and images. While running, Innervate will make requests to
deploy, scale, and undeploy services using one or more images. The
behavior of all of this, including what scenarios are run and which
users are used, is driven by the configuration file.

## Installation

### Docker Image

Releases of Innervate are uploaded to [Docker Hub](https://hub.docker.com/)
and can be found at: https://hub.docker.com/r/jdob/innervate/

Image builds will use the default configuration file which makes some
assumptions about the users and hostname of the OpenShift host. The
default host will resolve when deployed into an OpenShift instance.

The following environment variables are supported for further customizing
the container:

- `INNV_HOST`: Indicates the OpenShift host on which API calls will be made.
- `INNV_CONFIG`: URL to the configuration file to use when starting the Innervate engine

### From Source

Innervate is written in Python, meaning all normal Python installation
conventions apply. It is recommended that the application be installed
into a virtual environment. An example of the pip command, executed from
the project root directory, is below:
```
pip install -r requirements.txt -e .
```
Additionally, `-r test-requirements.txt` may be specified if the
unit tests will be run.

This installation process will add an executable called `innv` which
can be used to start the engine.
