# Ops Exercise

# Functions
# Fail deploy if something bad happened
def fail_deploy(logger):
    logger.debug("Failing deployment...")
    call(["/usr/local/bin/docker-compose","down"])
    return -1

# Print the exception caught
def print_exception(error,logger):
    logger.error(error)
    traceback.print_exc()

# Setup logging for the script
def setup_logging():
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    
    level = logging.getLevelName('DEBUG')
    rootLogger.setLevel(level)
    
    fileHandler = logging.FileHandler("{0}/{1}.log".format(logpath, logname))
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    
    return rootLogger

def main():
    # Set logging
    rootLogger = setup_logging()
    
    rootLogger.debug("test debug")
    
    # Make sure images directory exists and is empty
    if os.path.exists(images_dir):
       shutil.rmtree(images_dir)
    os.makedirs(images_dir)    
    
    # Download the images file
    try:
        filename = bucket.split("/")[-1]
        with open(filename, "wb") as f:
            r = requests.get(bucket)
            if r.status_code == 404:
               raise FileNotFoundError
            f.write(r.content)
    except Exception:
        print_exception("Error getting the images file.",rootLogger)
        fail_deploy(rootLogger)
    
    # Untar the images archive to public/images
    try:
        tar = tarfile.open(pics_tar,"r:gz")
        tar.extractall(images_dir)
        tar.close()
    except Exception:
        print_exception("Error extracting the images to public/images",rootLogger)
        fail_deploy(rootLogger)
    
    # Run docker-compose up
    try:
        call(["/usr/local/bin/docker-compose","up","-d"])
    except:
        print_exception("Error: docker-compose up command failed.",rootLogger)
        fail_deploy(rootLogger)

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
           print_exception("Health check failed.",rootLogger)
           fail_deploy(rootLogger)
    
    return 0

# Params
bucket = "https://s3.eu-central-1.amazonaws.com/devops-exercise/pandapics.tar.gz"
pics_tar = "pandapics.tar.gz"
images_dir = 'public/images/'
health_url = 'http://localhost:3000/health'
logpath = "/var/log"
logname = "ops-exercise"

# Imports
import requests,tarfile,urllib2,time,traceback,os,shutil,logging,sys
from subprocess import call

################
# SCRIPT BEGIN #
################

if __name__ == "__main__":
   sys.exit(main())


