# Ops Exercise

# Functions
def fail_deploy():
    print "Failing deployment....."
    call(["/usr/local/bin/docker-compose","down"])

def print_exception(error):
    print error 
    traceback.print_exc()

# Params
bucket = "https://s3.eu-central-1.amazonaws.com/devops-exercise/pandapics.tar.gz"
pics_tar = "pandapics.tar.gz"
images_dir = '/home/ec2-user/repo/Ops_Exercise/public/images/'
health_url = 'http://localhost:3000/health'

# Imports
import requests,tarfile,urllib2,time,traceback
from subprocess import call

################
# SCRIPT BEGIN #
################

# Download the images file
try:
    filename = bucket.split("/")[-1]
    with open(filename, "wb") as f:
        r = requests.get(bucket)
        if r.status_code == 404:
           raise FileNotFoundError
        f.write(r.content)
except Exception:
    print_exception("Error getting the images file.")
    fail_deploy()

# Untar the images archive to public/images
try:
    tar = tarfile.open(pics_tar,"r:gz")
    tar.extractall(images_dir)
    tar.close()
except Exception:
    print_exception("Error extracting the images to public/images")
    fail_deploy()

# Run docker-compose up
try:
    call(["/usr/local/bin/docker-compose","up","-d"])
except:
    print_exception("Error: docker-compose up command failed.")
    fail_deploy()

# Give the app a few seconds to start
print "Starting up the app..."
time.sleep(5)

# Run the health check with a 5 seconds timeout
try:
    r = requests.get(health_url, timeout=5)
    health = r.status_code
    if health != 200:
       raise ValueError("Health check returned: " + str(health))
except Exception:
       print_exception("Health check failed.")
       fail_deploy()

