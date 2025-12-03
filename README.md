# microservices-project
Microservices project for a web catalog of films. Made for the assignment Tópicos Avanzados de Desarrollo Web (Advanced Topics in Web Development). Based in the following architecture

![architecture](./resources/arch.png)

All you need to do is run the app

    $ docker compose up --build

Download the MFlix sample data
    
    $ curl  https://atlas-education.s3.amazonaws.com/sampledata.archive -o sampledata.archive

And import import it with `mongorestore`

    $ mongorestore --username admin --password 12345 --authenticationDatabase admin --archive=sampledata.archive --port=27017

Note: to use `mongorestore` you need the MongoDB Command Line Database Tools. You can download it from [MongoDB Download Center](https://www.mongodb.com/try/download/database-tools) and install it

### Notes

The microservices are implemented in the following way:

- Movies: GraphQL + Express
- RandomMovies: Flask
- Frontend: Vue.js
- Calificacion: Express
- Opiniones: Javascript
- Recomendador: Python + FastAPI

The goal was show the nature of the microservices architecture, where each microservice is idependent each other, even in stack.

The recommendation strategy is as follows:
- If the user has no rating made, it recommends to him the top rated movies
- If the user had rated movies, it recommends to him movies based in his ratings

### Future work

- There is aesthetic matters that I didn't get around to fixing it
- There is a problem with the posters: the database has posters, but the GraphQL service in Movies returns poster=null. I couldn't figure out why.