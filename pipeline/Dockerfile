FROM scilus/scilus-flows:1.5.0

# install the code
RUN mkdir -p /opt/run_tf
COPY ./run_tractoflow.py /opt/fwdti/
RUN chmod -R 775 /opt/fwdti

# set run command to call the script
ENTRYPOINT ["python", "/opt/run_tf/run_tractoflow.py"]
