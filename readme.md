Impetus
====================

This project is a cookie-cutter template for SocialCode dockerized Django projects.  The purpose of this tool is to simplify the initial overhead of creating new SocialCode projects.  The result of using this project is a functional application that can be deployed to all environments.

##Getting Started

These instructions describe how to get the advisor service running on your local machine for development and testing purposes. 

#### Prerequisites


#### SC Template Structure
```
.
├── [X] Dockerfile - Contains commands for setting up project docker image
├── [X] MANIFEST.in - Defines the list of files to include in the distribution built by the sdist command.
├── [X] Makefile - This is a build file, which for Make is called a Makefile
├── [X] README.md - Instructions and description of the project
├── [X] discovery_service
│   ├── [X] __init__.py
│   ├── [X] apps.py
│   ├── [X] authentication.py
│   ├── [X] clients.py
│   ├── [X] dev_settings.py
│   ├── [X] local_settings.py
│   ├── [X] migrations
│   ├── [X] models.py
│   ├── [X] pagination.py
│   ├── [X] permissions.py
│   ├── [X] serializers.py
│   ├── [X] settings.py
│   ├── [X] tests
│   ├── [X] urls.py
│   ├── [X] utils - Folder contains common methods and classes referenced throughout the application
│   ├── [X] views.py
│   └── [X] wsgi.py
├── [X] discovery_service_project - Folder containing project settings and manage.py
│   ├── [X] discovery_service_project - Typically generated locally during the projects first build.  These files are used to run manage.py from the root folder.  This is not a typical python project structure.  This file is also git ignored.
│   │   ├── [X] __init__.py
│   │   ├── [X] settings.py
│   │   ├── [NA] urls.py
│   │   └── [NA] wsgi.py
│   └── [X] manage.py
├── [X] docker-compose-jenkins.yml - A YAML file defining services, networks and volumes for the jenkins environment
├── [X] docker-compose.yml - A YAML file defining services, networks and volumes
├── [X] newrelic.ini.tmpl - New relic template that serves as an input for the New Relic configuration
├── [X] requirements.txt - Contains the pinned version of everything that was installed when pip freeze was executed.
├── [X] secrets.local.env - Contains database, authorization and the socialcode secrets references required to run app across environments. Relies on databag.  For more information ask TechOps.
├── [X] services
│   ├── [X] ${project-name}-service-web--alpha.json - AWS ec2 deployment configuration
│   ├── [X] ${project-name}-service-web--production.json - AWS ec2 deployment configuration
│   ├── [X] ${project-name}-service-web--qa1.json - AWS ec2 deployment configuration
│   ├── [X] ${project-name}-service-web--staging.json - AWS ec2 deployment configuration
│   ├── [X] docker-compose.alpha.yml - A server configuration reference that defines services, networks and volumes.
│   ├── [X] docker-compose.production.yml - A server configuration reference that defines services, networks and volumes.
│   ├── [X] docker-compose.qa1.yml - A server configuration reference that defines services, networks and volumes.
│   ├── [X] docker-compose.staging.yml - A server configuration reference that defines services, networks and volumes.
│   ├── [X] docker-compose.yml - A local server configuration reference that defines services, networks and volumes.
│   ├── [X] production.env - The file contains environment variables.
│   ├── [X] qa1.env - The file contains environment variables.
│   ├── [X] staging.env - The file contains environment variables.
│   └── [X] alpha.env - The file contains environment variables.
├── [X] settings.py.tmpl - A django settings template (used to create the settings.py file at build time.)
├── [X] setup.py - A `Disutils` python file that describes the module or project.
├── [X] uwsgi.ini.tmpl - A configuration file for uWSGI.


``` 

