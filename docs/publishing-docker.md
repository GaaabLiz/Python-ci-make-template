# Publishing to Docker Hub

This guide explains how to configure automatic Docker image publication to Docker Hub for each release.

---

## Prerequisites

### On Docker Hub

1. Create an account at [hub.docker.com](https://hub.docker.com/) if you do not already have one.
2. Create a repository from `Repositories -> Create Repository`.
   - Pick a name such as `myapp`. The full image name will be `yourusername/myapp`.
   - The repository can be public or private.
3. Generate an access token from `Account Settings -> Security -> New Access Token`.
   - A name such as `github-actions` is fine.
   - `Read & Write` permissions are enough.
   - Copy the token immediately because Docker Hub will not show it again.

### On GitHub

4. Create an environment in your repository from `Settings -> Environments -> New environment`.
   - Use the name `dockerhub` unless you also change `CI_DOCKERHUB_ENVIRONMENT` in `project.mk`.
   - Optional: add protection rules if your release process requires approvals.
5. Add these secrets to the `dockerhub` environment:

   | Secret | Value |
   |--------|-------|
   | `DOCKERHUB_USERNAME` | Your Docker Hub username |
   | `DOCKERHUB_TOKEN` | The access token created above |

---

## Template configuration

Update the relevant Docker settings in `project.mk`:

```makefile
CI_ENABLE_DOCKERHUB_PUBLISH ?= 1
CI_DOCKERHUB_IMAGE ?= yourusername/myapp
CI_DOCKERFILE ?= Dockerfile
CI_DOCKER_BUILD_CONTEXT ?= .
CI_DOCKER_PUSH_LATEST ?= 1
```

The sample multi-stage `Dockerfile` uses `CI_DOCKER_PYTHON_VERSION` and `CI_DOCKER_UV_VERSION`, which default to `CI_PYTHON_VERSION` and `CI_UV_VERSION`. Its default entrypoint runs the sample package with `python -m myapp`; change the module name if `PYTHON_MAIN_PACKAGE` changes:

```dockerfile
ENTRYPOINT ["python", "-m", "myapp"]
```

For a console-script application, replace it with the installed script:

```dockerfile
ENTRYPOINT ["myapp"]
```

---

## Local testing

Before enabling the release workflow, make sure the image builds and runs locally:

```bash
docker build -t myapp .
docker run --rm myapp --help
docker run --rm -it myapp
```

---

## How the workflow works

The workflow in `../.github/workflows/publish-dockerhub.yml` is called by `release.yml` after the CI gate, configured asset builds, and GitHub Release publication succeed. It runs only when `CI_ENABLE_DOCKERHUB_PUBLISH=1`.

The publication sequence is:

1. Log in to Docker Hub with the configured secrets.
2. Resolve the Docker tag from the verified Git tag.
3. Build the image with `docker build`.
4. Push the versioned tag.
5. Optionally push `latest` when `CI_DOCKER_PUSH_LATEST=1`.

After publishing `v1.2.3`, users can pull:

```bash
docker pull yourusername/myapp:v1.2.3
docker pull yourusername/myapp:latest
```

---

## Typical release flow

```text
make release-patch-tag
-> push tag v1.2.3
-> release.yml creates the GitHub Release
-> publish-dockerhub.yml builds and pushes the image
```

---

## Advanced customization

### Multi-platform builds

The workflow already installs Buildx, but the default Make target builds only for the runner architecture. To publish multiple architectures, extend `ci-docker-build` in the Makefile with a `--platform` flag such as `linux/amd64,linux/arm64`.

### Build arguments

If your Dockerfile needs build arguments, extend `ci-docker-build` like this:

```makefile
docker build \
    -f "$(CI_DOCKERFILE)" \
    --build-arg APP_VERSION=$$DOCKER_IMAGE_TAG \
    -t "$(CI_DOCKERHUB_IMAGE):$$DOCKER_IMAGE_TAG" \
    "$(CI_DOCKER_BUILD_CONTEXT)"
```

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---------|--------------|-----|
| Workflow does not start | `CI_ENABLE_DOCKERHUB_PUBLISH=0` | Set it to `1` in `project.mk` |
| Docker login fails | Missing or incorrect secrets | Check `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` in the environment |
| Docker build fails | `Dockerfile` not found | Verify that `CI_DOCKERFILE` points to the correct file |
| Push is denied | Token lacks write access | Regenerate the token with `Read & Write` permissions |
| Image is missing after push | Docker Hub repository does not exist | Create the repository before the first release |
| `latest` is not updated | `CI_DOCKER_PUSH_LATEST=0` | Set it to `1` in `project.mk` |
