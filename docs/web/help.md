# Modifying Help Page

If a change to the help page is required, the modification will become persistent after rebuilding the API image. Below are two procedures to make changes to the help page. It can be done with the server up or down. 

Live (keeps server up):
1. Modify `src/web/api/help.html`
2. Run `docker cp src/web/api/help.html api:/app/help.html`

Persistent (takes server down):
1. Modify `src/web/api/help.html`
2. Run `docker-compose down`
3. Run `docker-compose up --build`

