# Testing Google Cloud Run with CockroachDB

## Steps
1) Create You're own VPC
2) Create CC cluster
  - Create user
  - Create VPC peering between CC and VPC in step 1
3) Create VPC Serverless Connector
4) Deploy container in Google Cloud Run

## Step 1 - Create A New VPC for your Google Run app

In Google cloud, create a new VPC

_Console --> VPC Networks_
 
- Use a Custom subnet
- Dynamic Routing = Regional
- DNS Server Policy = None
- Private Google Access = Off (we should try with on)

**NOTE: Keep track of your CIDR range to know your range of IPs**

## Step 2 - Create a CockroachCloud Cluster

Add a new SQL User

Add a VPC Peering connection (need Project Id and name of VPC network created in Step 1)

Verify VPC Connection in your new VPC
```
gcloud --project cockroach-chrisc compute networks peerings create chrisc-cc-gcp --network=chrisc-vpc --peer-network=crdb --peer-project=crl-prod-5th --auto-create-routes
```

# Step 3 -  Create VPC Servlerless Connector

In Google console, go toS "Console" -> "Serverless VPC Access"

- Create in same region as created VPC
- Very important - when creating make sure that the CIDR range for the connector doesn't overlap with the VPC.

Choose the Route all traffic option?  Could we try this Private IP setup?

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
docker run -p 8080:8080 chriscasano/gcr
```

## Google Build 

Docs: https://cloud.google.com/run/docs/quickstarts/build-and-deploy?_ga=2.147364543.-903456326.1570542011

Add the container to the registry
```
gcloud builds submit --tag gcr.io/cockroach-chrisc/cctest
```

Deploy the container in Google Cloud Run

```
gcloud run deploy --image gcr.io/cockroach-chrisc/cctest --platform managed
```
Choose the region, service name and Y for allow unauthenticated invocations


## CC connection string
```
cockroach sql --url 'postgres://chris@clerk-test-5th.gcp-us-east4.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=<your_certs_directory>/clerk-test-ca.crt
```

#### install tools
```
apt-get update
apt-get install net-tools
apt-get install iputils-ping
```