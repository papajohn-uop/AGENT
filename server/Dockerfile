# 
FROM python:3.9

# 
WORKDIR /agent

# 
COPY ./requirements.txt /radio_mgmt_agent/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /radio_mgmt_agent/requirements.txt

# 
COPY ./src  /agent

# 
#CMD ["cd", "/radio_mgmt_agent/src"]
# cmd ["touch","do.ne" ]
# cmd ["touch","do.ne.2" ]
# CMD ["uvicorn", "openapi_server.main:app", "--host", "0.0.0.0", "--port", "80"]
# #CMD ["bash"]