# tautulli-epaper-display

The `tautulli-epaper-display` project connects with the Tautulli API and exhibits the returned status information on a display. The project is specifically designed to operate on a Raspberry Pi Zero with an attached 2.13" ePaper display.

## Local Development

### Prerequisites

* **This project requires [Python 3.11](https://www.python.org/downloads/release/python-3113/).**

* Dependencies are managed using [Poetry](https://python-poetry.org/docs/#installation). If you haven't installed it yet, use this command:

    ```shell
    pip install poetry
    ```

* [Pre-commit](https://pre-commit.com/) is used to enforce code quality. If you don't have pre-commit installed, you can install it using the following command:

    ```shell
    pip install pre-commit
    ```

### Setting up the Development environment

1. Initialize pre-commit:

    ```shell
    pre-commit install
    ```

2. Install dependencies and activate the virtual environment:

    ```shell
    poetry install
    poetry shell
    ```

### Running Tests

After activating the virtual environment with the command `poetry shell`, use the following command to run tests:

```shell
pytest
```

## Installation

### Pre-requisites

Regardless of what OS is used for the Raspberry Pi, the following must be installed:

* [Docker](https://docs.docker.com/engine/install/raspbian/).
* [Docker-compose Plugin](https://docs.docker.com/compose/install/linux/)

### Install Steps

1. Clone this repository to the Raspberry Pi.
2. Access the Raspberry Pi configuration interface by running this command:

    ```sh
    sudo raspi-config
    ```

3. Navigate to `Interfacing Options` -> `SPI` -> `Yes Enable SPI interface`.

4. Get the Tautulli URL and API key and store it as an environment variable by following these commands:

    ```sh
    # Open the bashrc file
    sudo nano ~/.bashrc
    ...
    # Add the following lines at the end of the file
    export TAUTULLI_URL='<TAUTULLI URL>'
    export TAUTULLI_API_KEY='<YOUR API KEY>'
    ```

5. Reboot the Rpi:

    ```sh
    sudo reboot
    ```

6. Run the following commands while in the root of the cloned repository:

    ```sh
    docker-compose up -d
    ```

## References

The project was built with some help from the [official Waveshare documentation](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_Manual#Working_With_Raspberry_Pi).
