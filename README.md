# Assignment7
Prometheus Assignment

Steps :

1. Install Prometheus and Grafana using Docker (with docker-compose).<br>
   Create a docker-compose.yml file and pull the Prometheus and Grafana images from DockerHub.

2. Configure prometheus (scrape configs) such way that it can scrape the metrics from default metric path of the application job.<br>
   Create a Microservice for scraping the metrics and also create a prometheus.yml file and add the scrape intervals and scrape configs.

3. Validate the entire configuration to check if the data is coming or not in Prometheus UI.<br>
   Open http://localhost:9090 and access the Prometheus Homepage and select Status and then go to Targets.

5. Create the Dashboards in Grafana on top of the metrics exported by adding the Prometheus as a Datasource.<br>
   Open http://localhost:3000 to access your Grafana Dashboard.
   Add your first data source, select Prometheus and enter the Prometheus server URL and then save and test.
   Now build a Dashboard and new Visualization and select Prometheus in that and select the Metric and press Run Queries.

