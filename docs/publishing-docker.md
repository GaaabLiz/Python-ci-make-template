# Publishing to Docker Hub

Docker packages an app together with the files it needs. Docker Hub is a service that stores these packages (called images) so people can download and run them. This publishing option is off by default.

## 1. Create a Docker Hub repository

1. Sign in to [Docker Hub](https://hub.docker.com/) and create a repository, for example `myapp`.
2. Create a [Docker Hub personal access token](https://docs.docker.com/security/access-tokens/personal-access-tokens/) and give it permission to push images to the repository.

## 2. Save the login details in GitHub

In your GitHub repository, open **Settings → Environments** and create an environment named `dockerhub`. An environment is a named place for release settings and private secrets. Add these two secrets to that environment:

| Secret name | Value |
| --- | --- |
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | The access token you just created |

Secrets are private values. Do not put them in `project.mk`, `Makefile`, or `Dockerfile`.

## 3. Set the project values

Edit the existing Docker settings in `project.mk`:

- Set `CI_ENABLE_DOCKERHUB_PUBLISH` to `1`.
- Set `CI_DOCKERHUB_IMAGE` to `your-username/your-repository`.
- Change `CI_DOCKERFILE` or `CI_DOCKER_BUILD_CONTEXT` only if your files are in different places.
- Set `CI_DOCKER_ENTRYPOINT` to the command that starts your app in the container. The default is `python -m $(PYTHON_MAIN_PACKAGE)`.
- Set `CI_DOCKER_PUSH_LATEST` to `1` if you also want a `latest` tag.

For example, if your package is started with `python -m myapp`, the default command works. If it has an installed command named `myapp`, set `CI_DOCKER_ENTRYPOINT` to `myapp`. Package-specific Docker settings belong in `project.mk`; the shared image build command is in `Makefile`.

## 4. Publish a release

Push a version tag such as `v1.2.3`. After the release checks pass, GitHub builds and pushes an image with that version. If enabled, it also pushes `latest`.

Users can download the image with:

```sh
docker pull your-username/your-repository:v1.2.3
```

## Optional: test the image locally

Install Docker Desktop or Docker Engine. Set `CI_DOCKERHUB_IMAGE` in `project.mk` to a local image name, such as `myapp-local`, then build and run it from Git Bash, WSL, macOS, or Linux:

```sh
DOCKER_IMAGE_TAG=local make ci-docker-build
docker run --rm myapp-local:local --help
```

Replace `myapp-local` in the last command with the image name you set in `project.mk`.

If the image fails to build, check that the `Dockerfile` path, build context, and app entry point match the project.
