# Django fixtures to initialize data


## Initialize data using fixtures (vnoi_website)
Run command:

```bash
	./init_database.sh
```

# Read more...

## How to create fixtures

1. Use Django Admin to create a database
2. Use Django dumpdata to create a fixture in desired format (json, yaml,..), and save into main/fixtures/appname.\*, or main/fixtures/modelname.*
   
   For example, to create a fixture of forum app in json format:
  
   ```bash
   		python manage.py dumpdata forum > main/fixtures/forum.json
   ```
   
## How to initialize data using fixture

1. Delete database: 

	```bash
		 rm db.sqlite3
	```	 
2. Use django migrate to create data tables

   ```bash
		python manage.py migrate 
   ```
   
3. Load data from fixtures

	```bash
		python manage.py loaddata auth.json
		python manage.py loaddata forum.json
	```
	- <!> Fixtures can be load only if all records satisfy database fields' requirements.	
	