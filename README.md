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

## Users

The users section contains a list of username/password combinations to use
when running scenarios. A user will be randomly selected from this list on
each loop through the engine.

The users are specified as a YAML list of tuples containing `username` and
`password`. Example:
```
users:
  - username: user1
    password: user1
  - username: user2
    password: user2
```

## Scenarios

The scenarios section defines all of the possible scenarios that may be
executed by the engine. On each loop, the engine will randomly choose
a scenario to execute.

If the scenario cannot be run because of the current
state of the system (e.g. attempting to delete a project when the user does not
have one deployed), another scenario is chosen.

Each scenario consists of four parts:

* `name`: Used for logging purposes only, this must be unique for each defined
  scenario.
* `type`: Indicates which scenario to execute. Multiple scenarios may be defined
  with the same type and specifying different configurations for each.
* `weight`: Drives the frequency at which this scenario will attempt to be
  executed. A higher weight means the scenario is more likely to be executed.
* `config`: Dictionary of values used to configure how the scenario runs. The
  possible configuration values is determined by the scenario type.

### Scenario Types

The following scenarios are supported:

#### CreateProject

Creates a new project for a given user. The name of the project is randomly
generated.

Configuration:

* `max_projects_per_user`: Upper limit to how many projects may be deployed
  for each user. If the scenario attempts to create a project on a user that
  is at this limit, the scenario is skipped.

#### CreateService

Deploys a service against an existing project. Currently, only images may
be deployed; S2I builds are not yet supported.

Configuration:

* `max_services_per_project`: Upper limit to how many services may be deployed
  for a given project. If the scenario attempts to create a service and finds
  the project is already at capacity, this scenario will be skipped.
* `images`: List of images that will be deployed as services. Each entry in
  the list contains:
  * `name`: Name of the image. Example: kubernetes/guestbook
  * `ports`: Port and protocol for the ports associated with the image.
  Example: 3000:TCP

#### ScaleUp

Scales the number of pods for an existing service up.

Configuration:

* `max_pods_per_service`: Upper limit to how many pods can be set for a given
  service. If the scenario attempts to scale a service that is already at
  this limit, the scenario will be skipped.

#### DeleteProject

Deletes a project for the given user.

#### DeleteService

Deletes a service from a random project under the given user.

#### ScaleDown

Reduces the number of pods for a given service. The pod count will not
be lowered below 1.

