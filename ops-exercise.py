# Ops Exercise

# Functions
def fail_deploy():
    print "Failing deployment....."
    call(["/usr/local/bin/docker-compose","down"])

import requests,tarfile,urllib2,time,traceback
from subprocess import call

# Params
url='http://localhost:3000/health'

# Download the images file
url = "https://s3.eu-central-1.amazonaws.com/devops-exercise/pandapics.tar.gz"
filename = url.split("/")[-1]
with open(filename, "wb") as f:
    r = requests.get(url)
    f.write(r.content)

# Untar the images archive to /public/images
tar = tarfile.open("pandapics.tar.gz","r:gz")
tar.extractall("./public/images")
tar.close()

# Run docker-compose up
call(["/usr/local/bin/docker-compose","up","-d"])

# Give the app a few seconds to start
print "Starting up the app..."
time.sleep(5)

# Run the health check with a 5 seconds timeout
try:
    r = requests.get(url, timeout=5)
    health = r.status_code
    if health != 200:
       raise ValueError("Health check returned: " + str(health))
except Exception:
    print "Exception caught:"
    traceback.print_exc()
    fail_deploy()

