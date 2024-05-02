# pyDagFlow

pyDagFlow is a Python library for creating and running directed acyclic graphs (DAGs) of tasks. It is inspired by Apache Airflow, but is designed to be lightweight and easy to use. 

pyDagFlow is build on top of pypubsub. It uses the observer pattern to notify tasks when their dependencies are complete. 

## Installation

```bash
git clone ...
cd pyDagFlow    
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Workflow and DTO (Data Transfer Object)

The workflow can be defined in two ways: a `.yaml` or a `.json` file. The `.json` can be obtained from the yaml using the `yaml2json.py` script in the `utils` folder:
    
```bash
python yaml2json.py <yaml_file> <json_file>
```

The following is an example of a `testflow.yaml` file:

```yaml
name: testflow
createdAt: 24-05-01 16:27:00
nodes:
  - 1: User,user
  - 2: Username,username
  - 3: Phone,phone
  - 4: Customer,customer
  - 5: Product,product
  - 6: Order,order
  - 7: Purchase,purchase
flow: 
  - 1>>2,3
  - 2,3>>4
  - 4,5>>6
  - 6>>7
inputs:
  - User: 
      name: John Doe
      phone: 123-456-7890
      email: john.doe@gmail.com
  - Product:
      product: beer
      price: 10
```

## functions 

The nodes of the workflow are defined as functions. For example, the following is the function that defines the nodes in the workflow above:

```python
def user(input:dict) -> dict:
    print("user: get user data")
    print(input)
    return input

def username(input:dict) -> str:
    username = input['User']['email'].split('@')[0]
    print("username: get username from email")
    return username

def phone(input:dict) -> str:
    print("phone: get country code from phone number")
    return input['User']['phone'].split('-')[0]

def customer(input:dict) -> dict:
    print("customer: get customer data")
    print(input)
    return {'username': input['Username'], 'country_code': input['Phone']}

def product(input:dict) -> dict:
    print(input)
    print("product: get product data")
    return input

def order(input:dict) -> dict:
    print(input)
    print("order: get order data")
    return {'customer': input['Customer']['username'], 'product': input['Product']['product'], 'price': input['Product']['price'], 'status': 'pending'}

def purchase(input:dict) -> dict:
    print(input)
    print("purchase: get purchase data")
    return {'customer': input['Order']['customer'], 'product': input['Order']['product'], 'price': input['Order']['price'], 'status': 'completed'}
```

## Running the workflow

then the workflow can be processed using the following command:

```bash
python run-flow.py ./dto/exampleDTO.json
```
functions (nodes) can be found in `functions` folder, aditional functions can be added to the `functions` folder and imported in the `flowFunctions.py` script.

the DTO is updated as the tasks are completed. 

## Complementary functions 

complementary functions are to be found in PyDagFlow-q71.