# Assignment7
Prometheus Assignment

Steps :

1. Install Prometheus and Grafana using Docker (with docker-compose).<br>
   Create a docker-compose.yml file to pull the Prometheus and Grafana images from DockerHub.

2. Configure prometheus (scrape configs) such way that it can scrape the metrics from default metric path of the application job.<br>
   Create a Microservice for scraping the metrics and also create a prometheus.yml file and add the scrape intervals and scrape configs.

3. Validate the entire configuration to check if the data is coming or not in Prometheus UI.<br>
   "sudo docker-compose up -d" command to start the Prometheus and Grafana server.<br>
   Open http://localhost:9090 and access the Prometheus Homepage and select Status and then go to Targets.
   ![image](https://github.com/AmoghBari/Assignment7/assets/145555795/afb5dffd-20c9-485f-b05a-c39e2d9eda7b)
   You can also see the metrics by clicking the Endpoint link.
   ![image](https://github.com/AmoghBari/Assignment7/assets/145555795/814b83df-2456-4cfc-bab0-c86c3e79f001)



5. Create the Dashboards in Grafana on top of the metrics exported by adding the Prometheus as a Datasource.<br>
   Open http://localhost:3000 to access your Grafana Dashboard.<br>
   Add your first data source, select Prometheus and enter the Prometheus server URL and then save and test.<br>
   Now build a Dashboard and new Visualization and select Prometheus and select the Metric and press Run Queries.
   ![image](https://github.com/AmoghBari/Assignment7/assets/145555795/8c3344bf-857e-44a8-80e4-7e7c7dd0d5e5)


