# tap-matomo

`tap-matomo` is a Singer tap for matomo.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

<!--

Developer TODO: Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPI repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.

## Installation

Install from PyPI:

```bash
uv tool install tap-matomo
```

Install from GitHub:

```bash
uv tool install git+https://github.com/ORG_NAME/tap-matomo.git@main
```

-->

## Configuration

### Accepted Config Options

<!--
Developer TODO: Provide a list of config options accepted by the tap.

This section can be created by copy-pasting the CLI output from:

```
tap-matomo --about --format=markdown
```
-->

## Capabilities

- `catalog`
- `state`
- `discover`
- `activate-version`
- `about`
- `stream-maps`
- `schema-flattening`
- `batch`
- `structured-logging`

## Supported Python Versions

- 3.10
- 3.11
- 3.12
- 3.13

## Settings

| Setting | Required | Default | Description |
|:--------|:--------:|:-------:|:------------|
| api_url | True | None | The url for the API service |
| token_auth | True | None | The token to authenticate against the API service |
| idSite | True | None | The integer id of your website, or a comma-separated list of idSites, e.g. idSite=1,4,5,6 |
| method | False | Live.getLastVisitsDetails | The API method you want to call. |
| period | False | day | The period you request the statistics for. Can be any of: day, week, month, year or range. All reports are returned for the dates based on the website's time zone. |
| date | False | None | standard format = YYYY-MM-DD or magic keywords = today, yesterday, lastWeek, lastMonth or lastYear. These are relative the website timezone.  |
| format | False | json | Defines the format of the output. |
| filter_limit | False | None | defines the number of rows to be returned, By default, only the top 100 rows are returned,Set to -1 to return all rows |


```bash
tap-matomo --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

Refer to the [Matomo API Authentication documentation](https://developer.matomo.org/api-reference/reporting-api#Live).

## Usage

You can easily run `tap-matomo` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-matomo --version
tap-matomo --help
tap-matomo --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

Prerequisites:

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

```bash
uv sync
```

### Create and Run Tests

Create tests within the `tests` subfolder and
then run:

```bash
uv run pytest
```

You can also test the `tap-matomo` CLI interface directly using `uv run`:

```bash
uv run tap-matomo --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

<!--
Developer TODO:
Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any "TODO" items listed in
the file.
-->

Use Meltano to run an EL pipeline:

```bash
# Install meltano
uv tool install meltano

# Test invocation
meltano invoke tap-matomo --version

# Run a test EL pipeline
meltano run tap-matomo target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
