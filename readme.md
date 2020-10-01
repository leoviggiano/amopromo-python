# How to Setup - Python Application
```sh
    $ git clone
    $ cd to folder
    $ virtualenv venv --python=3.8  #Depende da versão do python
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ docker-compose up -d
    $ python manage.py migrate
    $ python manage.py runserver
```

# Rotas:

## Airports
  - /airports/distance/ - **GET**
        - Rota definida para recuperar os aeroportos mais distante e mais perto

- /airports/count/ - **GET**
        - Rota definida para recuperar a quantidade de aeroporto por cidade

- /airports/seeds/ - **POST**
        - Rota definida para preencher o bacno de dados com os aeroportos disponibilizados

## Flights
- /flights/duration/ - **GET**
        - Rota definida para recuperar a duração do vôo, modelo de aeronave, local e destino. É ordenada pela duração do vôo de forma decrescente

- /flights/seeds/ - **POST**
        - Rota definida para preencher o banco de dados com os dados de vôos disponibilizados
        - Nota: Só é possível depois de preencher a tabela Airports
