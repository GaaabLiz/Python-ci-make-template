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

The template includes a sample multi-stage `Dockerfile` for Python CLI applications. Adjust the entrypoint to match your project:

```dockerfile
ENTRYPOINT ["myapp"]
```

If your package does not expose a console script, use the module entrypoint instead:

```dockerfile
ENTRYPOINT ["python", "-m", "myapp"]
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

The workflow in `../.github/workflows/publish-dockerhub.yml` runs when:

- a `v*` tag is pushed, for example `v1.2.3`
- the workflow is started manually with `workflow_dispatch`

The publication sequence is:

1. Read configuration from `project.mk` with `make ci-export-config`.
2. Continue only when `CI_ENABLE_DOCKERHUB_PUBLISH=1`.
3. Log in to Docker Hub with the configured secrets.
4. Resolve the Docker tag from the Git tag or fallback version.
5. Build the image with `docker build`.
6. Push the versioned tag.
7. Optionally push `latest` when `CI_DOCKER_PUSH_LATEST=1`.

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
