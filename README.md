# NobaNG
RPG based on a board game.

Setting up the development environment is required to make the experiments.
[Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)

1. Install "pipenv" [Windows](https://www.pythontutorial.net/python-basics/install-pipenv-windows/)
2. Copy Pipfile and "pfile.lock" to project directory.
3. Open command line in project directory.
4. Execute `pipenv install --ignore-pipfile`

# AWS Set-up
## Configure Networking
All these configuration is done in the Amazon Console and it is adviced to select a 3-5 letters prefix to distinguish the settings created in this section from any other setting that were already in the console:
 - [https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Instances:](https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Instances:)

1. First of all, create a virtual private cloud (VCP), mine has the following values ---make sure the intended Availability Zone is selected:
  * IPv4 CIDRs: 10.1.0.0/16
  * IPv6 CIDRs: <empty>
  * Once VPC is created, go to the "Your VPCs" page and make sure "Edit DNS hostnames" and "Edit DNS resolution" are both Enabled (from "Actions" menu)
2. Create an "Internet Gateway" (look for that name in the VPCs page) and assign it to the VPC:https://console.aws.amazon.com/vpc/home?region=us-east-1#RouteTables:
3. Create a Route Table and associate it to the VPN:
  * Routes:
    - Destination:10.1.0.0/16 (see how it corresponds to the VPC CIDR); Target: local (this will route traffic in the EC2 network)
    - Destination: 0.0.0.0/0 (everybody); Target: Select the Internate Gateway from previous step (this will rout traffic comming from Internet).
4. Create a Network ACL:
  * Add an *Inbound* rule to allow HTTP(port 80) and HTTPs(port 443) traffic.
  * Add an *Outbound* rule to provide the same access.
5. <span style="color: red;">This step is key to allow access to the EC2 instance: Create a "Security Group". Since VPC works with IPv4 addresses <span style="text-decoration:underline">only select IPv4 rules</span> remove any IPv6 one:
  * Add an *Inbound* rule to allow HTTP(port 80) and HTTPs(port 443) traffic.
  * Add an *Outbound* rule to provide the same access.
  * Add another set of Inbound/Outbound rules for SSH(port 22)</span>.
6. Create a couple subnets for the VPC:
  * Subnet to enable external access:
    - Name: public
    - IPv4 CIDRs: 10.1.1.0/24
    - Associate to the VPC, Route Table and Network ACL created in previous steps. <span style="text-decoration:underline">**Important:** By associating this subnet to the Route Table,the subnet will be accessible from the Internet</span>.
  * Subnet for internal networking only: 
    - Name: private
    - IPv4 CIDRs: 10.1.1.0/24
    - Associate the VPC and Network ACL created in previous steps. <span style="text-decoration:underline">Do NOT associate the private network to the Route Table</span>. That way it will be hidden from the outside world.

## Create an EC2 instance
This part is done in the Instances view of AWS Console: [https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Instances:v=3](https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Instances:v=3)
 1. Go to "AMI Catalog" in the "Images" section of left panel and chose an Amazon Machine Image (AMI). I chosed an Ubuntu based one.
 2. Select the VPC created in previous section, the public subnet and <span style="text-decoration:underline">for **Auto-assign Public IP** choose **Enable**. </span>
 3. Be careful and select just the free-tier image, nothing more sophisticated is required; I selected *t2.micro* image type.
 3. When prompted what credentials to use, chose the RSA keys of your preference or create a new one. Ths step is required to access the VPC for development and maintenance. The document referenced in this link shows how to access the EC2 instance using PuTTY: [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html)

# Setup NobaNG Service
For now just login to the EC2 instance, install flask and provide a basic web page:
1. Login (see previous section)
2. Install required software 
> `sudo apt update`
> `sudo apt install python3-pip`
> `pip3 install flask`
> `sudo pip3 install flask`
3. Create a sample flask application (save it as *app.py*):
> ```python
from flask import Flask

app = Flask(__name__)

# Defining the home page of our site
@app.route("/")  # this sets the route to this page
def home():
        return "Hello! this is the main page <h1>HELLO</h1>"  # some basic inline html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
```
4. Start the sample application `sudo flask run --host="0.0.0.0" --port=80`
5. Go to the EC2 instance and open the public DNS/IP

# Useful links
 * [Python Tutorial: Pipenv - Easily Manage Packages and Virtual Environments](https://www.youtube.com/watch?v=zDYL22QNiWk)
 * [Pipenv: A Guide to the New Python Packaging Tool](https://realpython.com/pipenv-guide/)
 