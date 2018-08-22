# BigPanda Ops Exercise
#### Ofri Sherf
#

------------------------------------------

> NOTE: I am fetching AWS Instance Metadata in the script in order to get the host's IP. If you are not using AWS, you will need to change **line 22** in the script.
-------------------------------------------

##### What I did
1. I created an EC2 instance on my account (RHEL 7)
2. Installed Docker
3. Created a docker-compose.yml template
4. Written the Python script

#

------------------------------------------------------
##### The Repo Contents
In addition to what was in the original repo I cloned, I added several files and directories:
1. `templates` directory
2. `templates/template.yml`: docker-compose template to be used
3. `public/images` directory
4. `ops-exercise.py`: the script to run
5. `docker-compose.yml`: was created by the script from the template

-------------------------
##### How to run the script
`sudo python ops-exercise.py`

------------------------------------------
##### Other Notes
Python version I used: 2.7.5
