# Innervate

Innervate is a chaos engine for simulating user interactions with
services and images. While running, Innervate will make requests to
deploy, scale, and undeploy services using one or more images. The
behavior of all of this, including what scenarios are run and which
users are used, is driven by the configuration file specified at runtime.

# Installation

## Docker Image

Releases of Innervate are uploaded to [Docker Hub](https://hub.docker.com/)
and can be found at: https://hub.docker.com/r/jdob/innervate/

Image builds will use the default configuration file which makes some
assumptions about the users and hostname of the OpenShift host. The
default host in that configuration will resolve when deployed into an
OpenShift instance.

The following environment variables are supported for further customizing
the container:

- `INNV_HOST`: Indicates the OpenShift host on which API calls will be made.
- `INNV_CONFIG`: URL to the configuration file to use when starting the Innervate engine

## From Source

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

# Usage

## Docker Image

Once deployed, the Innervate engine will begin to run and will continue
to do so until the container is destroyed.

## From Source

When run outside of a Docker image, the Innervate engine is started using
the `innv` command. It will continue to run and can be gracefully stopped
by pressing `^C`. By default, when gracefully stopped, the engine will delete
all deployed projects for the configured users (this can be controlled via
the `engine -> auto_clean` flag in the configuration file).

There are two flags available to the `innv` command:

- `-s`: Displays the current state (projects, services, and counts) for each
  user referenced in the configuration file.
- `-l`: Triggers the clean up operation which will delete all projects for
  the configured users.

# Configuration

The configuration file drives how the Innervate engine will behave. The
config/example.yaml file can be used as a starting point for customizing its
behavior.

## Engine

The engine configuration is used to customize the execution of the engine
loop.

* `scenario_sleep_range`: Minimum and maximum time, in seconds, to wait between
  scenarios. The engine will select a random time after each successful
  scenario is executed. The minimum and maximum values are separated with a
  hyphen. Example: 5-20
* `log_state_every`: If specified, the current state of the OpenShift
  installation will be logged in the scenario logging file after every X many
  scenarios. Example: 5
* `auto_clean`: If true, when the engine is gracefully stopped, all projects
  for each configured user will be deleted. Remove this configuration value
  to disable user clean up (clean up may be run from the command line at a
  later point if desired; see Usage).