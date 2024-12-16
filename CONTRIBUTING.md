Please open a pull request first, then ask to be assigned to it. We don't want
to be stepping on each other's toes while the project is under heavy 
development.

# Running this project in development mode
To make development easier, we've added a "development mode" for this project.
It does the following:
- Exposes the API endpoints of each service publicly, allowing you to use tools 
like Bruno to test them individually before integrating the endpoints with other
services.
- Enables hot-reload, for both front and back-end services.

See [README.md](README.md) to see how to run this project in development mode.

# Making changes to services
You have two options for your development environment when working on each of
the services:
- option 1: start the development container and connect to it using VSCode.
(Look this up if you don't know how to)
    - main benefit: you interact directly with the environment your service will run in
    - main issue: things like your VSCode extensions, language servers, etc. won't be available.
    - **NOTE:** Docker containers don't keep their state!! If you make changes to the environment (e.g. installing a package), make sure files like `Dockerfile` are up-to-date.
- option 2: install dependencies on the host and star developing
    - benefit: You can use all your tools
    - benefit: It's pretty easy to do with `uv` (for Python) and `npm` (for JS)
    - drawback: Issues may arise due to differences between your development environment and the container.
