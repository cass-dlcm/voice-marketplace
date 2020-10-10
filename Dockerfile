FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN mkdir /code
WORKDIR /code
RUN apt-get update \
        && apt-get install -y ca-certificates \
        && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
        && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
        && apt-get update \
        && ACCEPT_EULA=Y apt-get install msodbcsql17 mssql-tools -y \
        && apt-get install gcc g++ python3.7-dev unixodbc-dev -y \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# ssh
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
        && apt-get install -y --no-install-recommends openssh-server \
	&& echo "$SSH_PASSWD" | chpasswd \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

COPY Pipfile /code/
RUN pip install pipenv \
        && pipenv install
COPY . /code/

COPY sshd_config /etc/ssh/
COPY init.sh /usr/local/bin/

RUN chmod u+x /usr/local/bin/init.sh
EXPOSE 8000 2222
#CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["init.sh"]
