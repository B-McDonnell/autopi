# Modifying Help Page

If a change to the help page is required, it can be done with the server up or down. 
If the change is made while the server is up (*While server is live*), and a permament change is desired, complete procedure *Permanent change*.

While server is live (only tempororary change):
1. Modify src/web/api/help.html
2. Run `docker cp src/web/api/help.html api:/app/help.html`

Permanent change (takes server down):
1. Modify src/web/api/help.html
2. Run `docker-compose down`
3. Run 'docker-compose up --build`

