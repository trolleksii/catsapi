# Cat Catalog API Specs

## JSON Objects returned by API

All data are returned in JSON format.

### Cat breed

```JSON
{
  "status": "success",
  "message": {
    "name": "Abyssinian",
    "slug": "abyssinian"
  },
}
```


### Multiple cat breeds

```JSON
{
  "status": "success",
  "message": [
    {
      "name": "Abyssinian",
      "slug": "abyssinian"
    },
    {
      "name": "British Shorthair",
      "slug": "british-shorthair"
    },
    {
      "name": "British Longhair",
      "slug": "british-longhair"
    }
  ]
}
```


### Cat image

```JSON
{
  "status": "success",
  "message": "static/images/abyssinian/4887f792-796a-4f7d-b444-89c254f327c7.jpg"
}
```


### Multiple cat images

```JSON
{
  "status": "success",
  "message": [  
      "static/images/abyssinian/4887f792-796a-4f7d-b434-89c253f327c7.jpg",
      "static/images/abyssinian/69115af0-db84-4aa4-955e-17719f7e2b7b.jpeg",
      "static/images/abyssinian/5dc9bd98-3ad6-4a3b-802b-17d89118b7b5.png"
  ]
}
```

### Errors and status codes

All errors are returned in the following format:

```JSON
{
  "status": "error",
  "message": {
    "not_found": "Breed not found."
  }
}
```

Status code of response corresponds to the error type.



## API Endpoints

### Get list of available breeds:

`GET api/breeds`

Returns [Multiple cat breeds](#multiple-cat-breeds)


### Add a new breed to the list

`POST api/breeds`

Example request body:

```JSON
{
  "breed": {
    "name": "cornish rex"
  }
}
```

Returns a [Cat breed](#cat-breed) which was added


### Get a list of images of the specific breed

`GET api/breeds/:breed`

Returns [Multiple cat images](#multiple-cat-images)


### Get a random image of the specific breed

`GET api/breeds/:breed/random`

Returns a [Cat image](#cat-image)


### Upload an image of the specific cat breed

`POST api/breeds/:breed`

Use <b>multipart/form-data</b> to upload the one ore more images. Image size is limited to <b>500KB</b>
You should name your file(s) with the same name `files` in request, e.g.

```SH
curl -F files=@image1.jpg -F files=@image2.png localhost:8000/api/breeds/british-longhair
```

Returns a [Cat image](#cat-image) which was added
