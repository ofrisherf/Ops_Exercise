import requests,tarfile,urllib2,time,traceback
from jinja2 import Environment, PackageLoader,FileSystemLoader, select_autoescape
from subprocess import call

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

# Render the docker-compose.yml template
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('template.yml')

# Get the insntance IP address from AWS metadata
res = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4')
ipaddr = res.text
output_from_parsed_template = template.render(ip=ipaddr)
print output_from_parsed_template

# Save the results to a docker-compose.yml file
with open("docker-compose.yml", "wb") as fh:
    fh.write(output_from_parsed_template)

# Run docker-compose up
call(["/usr/local/bin/docker-compose","up","-d"])

url='http://' + ipaddr + ':3000/health'

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
    print "Failing deployment....."
    call(["/usr/local/bin/docker-compose","down"])
    pass

