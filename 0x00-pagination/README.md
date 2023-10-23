# ___0x00.Pagination___
This folder contains the actual results of completing the tasks in the project ___0x00.PAGINATION.___ The project was a introduction to pagination in REST API design. Pagination refers to the concept of splitting large chunks of data in a response into smaller chunks/multiple pages that the client can easily process. Types of pagination covered here are **offset/[simple](1-simple_pagination.py) pagination**, **keyset/[hypermedia](2-hypermedia_pagination.py) pagination**, and **seek/[deletion-resilient hypermedia](3-hypermedia_del_pagination.py) pagination**. 

The advanced pagination techniques used here involved **_Hypermedia as the engine of application state (HATEOAS)_**, which is a constraint of the REST application architecture that distinguishes it from other network application architectures. With HATEOAS, a client interacts with a network application whose application servers provide information dynamically through hypermedia. A REST client needs little to no prior knowledge about how to interact with an application or server beyond a generic understanding of hypermedia. This restriction imposed by HATEOAS decouples client and server, which allows server functionality to evolve independently. [Source: [Wikipedia](https://en.wikipedia.org/wiki/HATEOAS)]

## Technologies Used
1. Python

## Mandatory Tasks
There are four mandatory tasks in this project, comprised of python scripts (*.py), numbered 0 to 3, followed by a hyphen, then the name of the task the file corresponds to.

## Advanced Tasks
There are no advanced tasks in this project.
