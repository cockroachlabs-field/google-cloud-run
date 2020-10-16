# Google Cloud Run using a Serverless VPC Connector for CockroachCloud

## Steps

1) Create You're Own VPC in GCloud
2) Create CockroachCloud cluster
  - Create a SQL user
  - Create a VPC Peering between CockroachCloud and your new VPC in step 1
3) Create VPC Serverless Connector
4) Deploy a container in Google Cloud Run

## Step 1 - Create A New VPC for your Google Run app

In Google cloud, create a new VPC

_Console --> VPC Networks_

- Name = chrisc-vpc 
- Use a Custom subnet
- CIDR Range: 10.0.0.0/28 => 16 IPs
- Dynamic Routing = Regional
- DNS Server Policy = None
- Private Google Access = Off (we should try with on)
- Click Create
- Record your Project Id and the name of the new VPC


**NOTE: Keep track of your CIDR range to know your range of IPs**

## Step 2 - Create a CockroachCloud Cluster

Add a new SQL User

Add a VPC Peering connection (need Project Id and name of VPC network created in Step 1)

Verify VPC Connection in your new VPC.  The verification command should look something like this and is generated from the CockroachCloud VPC Peering "Connect" button:

```
gcloud --project cockroach-chrisc compute networks peerings create chrisc-cc-gcp --network=chrisc-vpc --peer-network=crdb --peer-project=crl-prod-5th --auto-create-routes
```

# Step 3 -  Create VPC Servlerless Connector

In Google console, go toS "Console" -> "Serverless VPC Access"

**Very important: When creating make sure that the CIDR range for the connector doesn't overlap with the VPC.  If you're not sure of your CIDR range, you can figure it using a CIDR calculator: https://www.ipaddressguide.com/cidr**

- Click "Create Connector"
- Give the connector a name: "cc-connector"
- Create in same region as created VPC
  - Region = us-east4
  - Network = chrisc-vpc (the name from Step 1)
- Click Create
- Validate the connector creates successfully

- Choose the Route all traffic option?  Could we try this Private IP setup?


### Verify if adding more permissions is neccessary...

```
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member=serviceAccount:service-$PROJECT_NUMBER@gcf-admin-robot.iam.gserviceaccount.com \
--role=roles/viewer

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member=serviceAccount:service-$PROJECT_NUMBER@gcf-admin-robot.iam.gserviceaccount.com \
--role=roles/compute.networkUser
```

# Step 4 - Run Google Run

## Local testing with docker
```
docker build -t chriscasano/gcr:latest .
export COCKROACH_URI="postgres://chris:<password>@clerk-test-5th.gcp-us-east4.cockroachlabs.cloud:26257/defaultdb?sslmode=require&sslrootcert=/app/certs/clerk-test-ca.crt"
docker run -p 8080:8080 --env COCKROACH_URI chriscasano/gcr
```

## Google Build 

Docs: https://cloud.google.com/run/docs/quickstarts/build-and-deploy?_ga=2.147364543.-903456326.1570542011

Add the container to the registry
```
gcloud builds submit --tag gcr.io/cockroach-chrisc/cctest
```


~~gcloud run deploy --image gcr.io/cockroach-chrisc/cctest --platform managed~~

~~Choose the region, service name and Y for allow unauthenticated invocations~~

Go to Cloud Run (GCP Console --> "Cloud Run") 

Click Create Service

Service Settings:
- Fully Managed, Region = us-east4
- Service name = cctest
- Allow unauthenticated invocations

Service Revisions:
- Choose your latest image
- In Advanced Settings -> Variables -> Add Variables
  - ```COCKROACH_URI = postgres://chris:<password>@clerk-test-5th.gcp-us-east4.cockroachlabs.cloud:26257/defaultdb?sslmode=require&sslrootcert=/app/certs/clerk-test-ca.crt```
- In Advanced Settings -> Connections -> VPC Connector
  - VPC Connector = Choose Custom
  - Select your serverless vpc connector = "cc-connector"
  - Select "Route All Traffic Through VPC Connector"

Deploy the container in Google Cloud Run

Once deployed, check the logs of the running container.  If you see this...

```
2020-10-16T01:40:12.832159Z  Connecting to database...
2020-10-16T01:40:13.011622Z  DB Connection Success
2020-10-16T01:40:13.014043Z  SQL Executed!
```

Then you can get the....
# Champagne!



#### Container debugging tools
```
apt-get update
apt-get install net-tools
apt-get install iputils-ping
```