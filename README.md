# drfAutoRiaScrap

### Start app

    docker-compose up --build

### Scrap pages and write results into darabase endpoint (returns the most epensive car from page )

`http://localhost:8000/autos/scrap/page/<int:pk>`

### Get cars from database

`http://localhost:8000/autos/all_cars`

### Filters example

`?price=[int,int]`
`?year=[int,int]`
`?mileage=[int,int]`
`?state_number=true` or `?state_number=false`
`order_by='-price` allowed values = ('price', '-price', 'year', '-year', 'mileage', '-mileage')

### request example

`http://localhost:8000/autos/all_cars/?price=[4000,14000]?year=[2010,2020]?state_number=true?order_by=-price`