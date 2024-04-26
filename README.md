## Project Overview

* Fast API (API Framework)

* PyTest (Testing Framework)

## Running the server

  Create a virtual environment

  Activate your virtual environment

  `git clone git@github.com:ranjitmarathay/vantagescore-challenge.git`

  `cd vantagescore-challenge`

  `pip install -r requirements.txt`

  `cd app`

  `uvicorn main:app --reload`


## Running the tests

  `pytest`


## Available Endpoints

### 1. List All Properties

- **Endpoint**: `GET /property`
- **Description**: Retrieves a list of all properties stored in the database.
- **Parameters**: None
- **Returns**: An array of property objects.
- **Example Response**:
  ```json
  [
    {
      "title": "Luxury Villa",
      "address": "123 Ocean Drive",
      "unit": "B",
      "property_value": 750000,
      "year_built": "1990",
      "bed": 3,
      "bath": 2,
      "sleeps": 6,
      "sqft": 2000,
      "lot_size": 5000,
      "description": "A beautiful seaside villa with stunning views.",
      "image_url": "https://example.com/images/villa.jpg",
      "url": "https://example.com/property/villa",
      "last_updated": "2024-04-26T04:54:17.673000Z",
      "nightly_rate": 450,
      "property_type": "House"
    }
  ]

### 2. Get a Single Property

- **Endpoint**: `GET /property/{property_id}`
- **Description**: Retrieves detailed information about a specific property by its ID.
- **Parameters**:
  - `property_id` (int): The unique identifier of the property.
- **Returns**: A single property object.
- **Example Response**:
  ```json
  {
    "title": "Luxury Villa",
    "address": "123 Ocean Drive",
    "unit": "B",
    "property_value": 750000,
    "year_built": "1990",
    "bed": 3,
    "bath": 2,
    "sleeps": 6,
    "sqft": 2000,
    "lot_size": 5000,
    "description": "A beautiful seaside villa with stunning views.",
    "image_url": "https://example.com/images/villa.jpg",
    "url": "https://example.com/property/villa",
    "last_updated": "2024-04-26T04:54:17.673000Z",
    "nightly_rate": 450,
    "property_type": "House"
  }

### 3. Create a Property

- **Endpoint**: `POST /property`
- **Description**: Adds a new property to the database.
### Required Body
- **Property** (object): A property object containing all necessary property details.
### Example Request Body

  ```json
  {
    "title": "Cozy Cottage",
    "address": "456 Mountain Road",
    "unit": "A",
    "property_value": 300000,
    "year_built": "1985",
    "bed": 2,
    "bath": 1,
    "sleeps": 4,
    "sqft": 1200,
    "lot_size": 2000,
    "description": "A cozy cottage in the mountains.",
    "image_url": "https://example.com/images/cottage.jpg",
    "url": "https://example.com/property/cottage",
    "last_updated": "2024-04-26T04:54:17.673000Z",
    "nightly_rate": 150,
    "property_type": "Cottage"
  }

### 4. Update a Property

- **Endpoint**: `PUT /property`
- **Description**: Updates an existing property.
### Required Body
- **Property** (object): Any number of fields in the Property Object
### Example Request Body

  ```json
  {
    "title": "Cozy Cottage",
    "address": "456 Mountain Road",
    "unit": "A",
    "property_value": 300000,
    "year_built": "1985",
    "bed": 2,
    "bath": 1,
    "sleeps": 4,
    "sqft": 1200,
    "lot_size": 2000,
    "description": "A cozy cottage in the mountains.",
    "image_url": "https://example.com/images/cottage.jpg",
    "url": "https://example.com/property/cottage",
    "last_updated": "2024-04-26T04:54:17.673000Z",
    "nightly_rate": 150,
    "property_type": "Cottage"
  }