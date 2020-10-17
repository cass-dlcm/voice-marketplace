FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN mkdir /code
WORKDIR /code
RUN apt-get update \
        && apt-get install -y ca-certificates \
        && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
        && wget -q -O - https://packages.blackfire.io/gpg.key | apt-key add - \
        && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
        && echo "deb http://packages.blackfire.io/debian any main" | tee /etc/apt/sources.list.d/blackfire.list \
        && apt-get update \
        && ACCEPT_EULA=Y apt-get install msodbcsql17 mssql-tools -y \
        && apt-get install gcc g++ python3.7-dev unixodbc-dev blackfire-agent -y \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# ssh
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
        && apt-get install -y --no-install-recommends openssh-server \
	&& echo "$SSH_PASSWD" | chpasswd \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install pipenv
COPY Pipfile /code/
RUN pipenv install --verbose --skip-lock
COPY y.txt /code/
RUN pipenv run python -m blackfire install-bootstrap < y.txt
COPY . /code/

COPY sshd_config /etc/ssh/
COPY init.sh /usr/local/bin/

RUN chmod u+x /usr/local/bin/init.sh
EXPOSE 8000 2222
#CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["init.sh"]
