# dmgrader
Data Mining Grader

# Turn-key installation instructions

## Requirements
1. Linux distribution for OS (these instructions may work on other OS, but tested on Redhat Linux, AWS AMI)
2. Python v3.7.0 (other version may work, but this is the version we used, no earlier than 3.5 is recommended)
3. Postgres version 8 or later from Postgres' website (https://www.postgresql.org/)
4. Latest version Docker and docker-compose installed from Docker's website (https://www.docker.com/)
5. The source code from this repo! Clone from `<insert public repo link here>`


## Quick-start instructions
Run the bash script located at `/dmgrader/deploy.sh`

`sh /dmgrader/deploy.sh [-Attributes]`




### Flag attributes
  - `-b`  build/rebuild everythings and start the project.  
  - `-s`  start project without any rebuild.   
  - `-m`  maintenance mode, do anything you like, e.g. command some docker commands.  
  - `-h`  echo the help instraction.  
  - `[nothing]`  default mode, start the project. If any images/containers required, build them.

  
### Database configuration
* Both the `settings.py` file and the `docker-compose.yml` file must match for database configuration.
    * The `settings.py` file should be located at path `/dmgrader/gradingwebapp/gmugrader/gmugrader/settings.py`
    * The `docker-compose.yml` file should be located at path `/dmgrader/gradingwebapp/gmugrader/dockerfiles/docker-compose.yml`
* The Postgres database port should default to port `5432`



