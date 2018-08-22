{{cookiecutter.project_label}}
=================


#### Prerequisites
Request the following variables (for each environment) before executing the cookiecutter template:
- services.${env}.sentry.dsn
- services.project_name-web--${env}.load_balancers.target_group_arn

#### Run a web server

    make web
    
#### Run all tests

    make test

#### Run pylint / pep8 checks

    make style

#### Running locally
  1.  Install (a default installation of) MySQL
  2.  Execute `make prereqs`
        1. The prereqs script requires the following:
            1.  An active [VPN session](https://socialcode.atlassian.net/wiki/spaces/techops/pages/92733679/Setup+VPN+Connection) (to access Social Code specific Wheel and Eggs)
            2.  A recent version of pip configured to use the Socialcode repo. See the [Confluence](https://socialcode.atlassian.net/wiki/spaces/techops/pages/95518775/Working+with+python-repo.socialcodedev.com#Workingwithpython-repo.socialcodedev.com-InstallingPackagesfromthePython-Repo)
            and [pip](https://pip.pypa.io/en/stable/user_guide/#configuration) documentation
            3.  Note: MySQL process should be running
        2. Note: The prereqs script creates a database user 'socialcode'.
  3. Create the **{{cookiecutter.application_name}}/local_settings.py**
