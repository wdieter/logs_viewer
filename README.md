# Log file reader service
This repository contains a REST API service to read log files stored under `/var/log/`

The primary entrypoint to the service is the `/logs` endpoint which takes the following parameters: 
- filename: name of file or directory to read logs from. if omitted, all logs from files under `/var/log/` will be returned recursively
- keyword: if set, returns only logs containing keyword, case-insensitive
- n: number of logs to return per log file

# Building and running the service:
To run the service first create a virtualenv to install the necessary dependencies

The following will create a virtualenv

```python3 -m venv ~/envs/cribl-venv```

Activate the virtualenv with 

`source ~/envs/cribl-venv/bin/activate`

Install dependencies

`pip install -r requirements.txt`


Run Tests:

```python -m unittest discover .```

If all the tests pass you can try running the service locally 

## Running web server locally

To run the webserver locally run: 
```flask --app service run```

Navigate to http://127.0.0.1:5000 and start searching for logs on your local computer!



Future improvements:
- Service improvements:
  - providing a list of files to filename arg
  - providing regex pattern read matching log file names
  - listing files under `/var/log` or subdirectories 
  - adding pagination so that the response size is not unbounded if a directory is specified
  - reading other logfile types in addition to .log (gzip files, bz2, asl)
  - perhaps having another param to suppress error messages from unsupported file types
- Deployment:
  - Containerizing the application to simplify building and running the webserver on different platforms
  - including a makefile to build and run containerized service
