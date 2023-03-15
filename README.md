# AAA Backend Homework
This is a simple flask application that reads the plate number from an image and returns the plate number in JSON format.

## API
- `GET /read-plate-number?img_id` - Returns the plate number in JSON format. `img_id` is the image id.
- `GET /read-plate-numbers?img_ids` - Returns the plate numbers in JSON format. `img_ids` is a comma separated list of image ids.

## Client
Client is a simple python wrapper for the API. It can be used as follows:
```python
from plate_reader_client import PlateReaderClient

client = PlateReaderClient('http://localhost:8080')
plate_number = client.read_plate_number(10022)
plate_numbers = client.read_plate_numbers([10022, 9965])
```

## Running the application
Application can be run using docker-compose. To run the application, run the following command:
```bash
docker build -t plate-reader .
docker-compose up
```

## Configuration
Configuration can be done using `config.ini` file. The following configuration options are available:
- `[App] name` - Name of the application.
- `[Run] debug` - Set to `True` to enable debug mode.
- `[Image Server] host` - Image server host. This is the host where the images are stored.
- `[Model] model_weights` - Name of the model weights file. This file should be present in the `model_weights` directory.
