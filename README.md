Flask Demo Movie API

To deploy 
- Open your terminal
- Simply head on to the Project directory
- enter "docker-compose up -d --build"

API End Points


GET - http://127.0.0.1:5000/services/<id>
returns movie summary

GET - http://127.0.0.1:5000/services?name=<name>
returns specific movie based on %name% search, case sensitive

PUT - http://127.0.0.1:5000/services/<id>
update movie info


