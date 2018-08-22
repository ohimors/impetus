FROM {{cookiecutter.docker_file__sc_docker_python_version}}
Maintainer applications@socialcodeinc.com

WORKDIR {{cookiecutter.docker_file__work_directory}}
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -r requirements.txt
RUN uwsgi --build-plugin https://github.com/unbit/uwsgi-sentry
RUN mkdir /etc/newrelic

COPY {{cookiecutter.application_name}}/ {{cookiecutter.application_name}}
COPY setup.py .
COPY *.tmpl ./
RUN python setup.py build install && rm -rf build/ dist/ {{cookiecutter.application_name}}/ {{cookiecutter.application_name}}.egg-info/

ENV SETTINGS_FILE=/var/{{cookiecutter.application_name}}/settings.py
ENV DJANGO_SETTINGS_MODULE=settings
ENV PYTHONPATH=/var/{{cookiecutter.application_name}}
ENV NEW_RELIC_CONFIG_FILE=/etc/newrelic/newrelic.ini

ENTRYPOINT [ \
    "dockerfy", "--verbose", \
    "--template", "/var/{{cookiecutter.application_name}}/settings.py.tmpl:/var/{{cookiecutter.application_name}}/settings.py", \
    "--template", "newrelic.ini.tmpl:/etc/newrelic/newrelic.ini", \
    "--template", "/var/{{cookiecutter.application_name}}/uwsgi.ini.tmpl:/var/{{cookiecutter.application_name}}/uwsgi.ini" \
    ]
