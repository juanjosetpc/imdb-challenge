The idea is to provide a solution that customers can use to get information from IMDb in a friendly manner.

The system has two parts:
- Ingestion of IMDb data
- Server and client to expose the data through requests for our customers

## High level requirements

It is required to have:
- A Process to ingest data from https://datasets.imdbws.com into the system (known as `system_module_1` from now on).
- Client-server architecture for scalability and stability (known as `system_module_2` from now on).

### Ingestion processing

For the `system_module_1` the developer can choose any programming language and framework.
The solution should be able to load/store IMDb data. It would also be useful to be able to clean up and reload the data.

### Client-Server

`system_module_2`'s server should offer a REST API that can be consumed by an application, or potentially any other services. Developer can use any programming language/framework.

`system_module_2`'s client is a CLI application for customers to query data from the `system_module_2` server and show the responses.

Implement:
- One endpoint get information about people
- Another endpoint to get information about films

Some examples:
- If a user requests information about "Bruce Lee", the response could be something like:
    - `Bruce Lee was born in 1940 and he was actor and producer.`
- If a user requests information about the "Blacksmith Scene" documentary, the response could be something like:
    - `Blacksmith Scene, originally titled 'Les forgerons', is a documentary.`

## Task

Assume I am a business man with an idea. I need you to create the product. The task is to build that system (`system_module_1` and `system_module_2`).

Important things:

- The goal is to have a production-ready solution.
- Take whichever decisions you need in order to build the product.
- Think that this system will be delivered to the integration team, QA team, delivery team...
- Pay attention to the user experience too.
- Concurrent sessions must be supported.
- Example of interaction is just a draft with the only purpose of showing the idea to the developer. Feel free to implement it in other way, with different requests, etc.
- The outcome of this task should have "Open Source" quality (i.e. what you expect when you reach to Github looking for a project)
- Some quality standards:
    - README file
    - User documentation
    - Implementation notes: what others need to know in order to be able to maintain the software
    - Unit tests
    - Performance will be observed and taken into account for both the data loading process and API queries.

**Bonus**: Apart from delivering the solution as a project in order to review the code and all content, you can optionally prepare the solution using `Docker` packaging the application and its dependencies into a container that can be run anywhere.

## Notes

If you think that something is required but, because of time constraints, it is not worthy to fully implement it, you can skip it and just prepare a good description of what should have been done, why, how, etc.