# Coffee Cart Interface
### Prerequisites
Docker and docker-compose

### To build and interact
Run `make` in the project directory. This builds and runs the docker containers. Make your way to `http://localhost:8000/api/v1/menu/` (the docker engine may not be listening on localhost, say if you are running on Windows).

### Test cases
Tests have been written in `coffee-cart/menu_backend/tests.py`. To run these tests: <br>
`docker ps` -> to find the docker container id of `coffeecart_web` <br>
`docker exec -it <container-id> bash` to "enter" the container <br>
Make your way to `/app/coffee-cart/` <br>
`python manage.py test menu_backend` to run test cases