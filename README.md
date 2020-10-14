# Testing Google Cloud Run with CockroachDB

## Steps
1) Create CC cluster
2) Create user
3) In your own GCP project, create a VPC
4) Create VPC peering between CC and VPC in step 3
5) Deploy container in Google Cloud Run

## Verify VPC Connection

gcloud --project cockroach-chrisc compute networks peerings create chrisc-cc-gcp --network=chrisc-vpc --peer-network=crdb --peer-project=crl-prod-5th --auto-create-routes

## Local testing with docker

docker build -t chriscasano/gcr:latest .
docker run -p 8080:8080 chriscasano/gcr

## CC connection string

cockroach sql --url 'postgres://chris@clerk-test-5th.gcp-us-east4.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=<your_certs_directory>/clerk-test-ca.crt


#### install tools
apt-get update
apt-get install net-tools
apt-get install iputils-ping
