# microservices-project
Microservices project for a web catalog of films. Made for the assignment Tópicos Avanzados de Desarrollo Web (Advanced Topics in Web Development). Based in the following architecture

![architecture](./resources/arch.png)

### Set up and running

All you need to do is run the app

    $ docker compose up --build

Download the MFlix sample data
    
    $ curl  https://atlas-education.s3.amazonaws.com/sampledata.archive -o sampledata.archive

And import import it with `mongorestore`

    $ mongorestore --username admin --password 12345 --authenticationDatabase admin --archive=sampledata.archive --port=27017

Note: to use `mongorestore` you need the MongoDB Command Line Database Tools. You can download it from [MongoDB Download Center](https://www.mongodb.com/try/download/database-tools) and install it

### Notes

The microservices are implemented as follows:

- **Movies:** GraphQL + Express
- **RandomMovies:** Flask
- **Frontend:** Vue.js
- **Calificacion:** Express
- **Opiniones:** Javascript
- **Recomendador:** Python + FastAPI

The goal was to showcase the nature of a microservices architecture, where each microservice is independent from the others, even in terms of technology stack.

The recommendation strategy works as follows:
- If the user has not rated any movies, the system recommends the top-rated movies.
- If the user has rated movies, the system recommends new movies based on those ratings.

### Future work
- There are aesthetic issues that I didn't have time to fix.
- There is a problem with the posters: the database contains poster data, but the GraphQL Movies service returns `poster = null`. I wasn’t able to determine the cause.