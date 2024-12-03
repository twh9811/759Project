FROM python:3.12-slim
WORKDIR /example
COPY process_inputs.py /app/process_inputs_example.py
# When the docker file executes from an GitHub Action it basically does 'docker run <image_name> arg1 arg2'
# This passes arg1 and arg2 into the CMD execution as well so it is running process_inputs with the args from the action as inputs.
# Taint Sink
CMD ["python", "/example/process_inputs_example.py"]
