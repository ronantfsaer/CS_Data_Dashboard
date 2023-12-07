from pydantic import BaseModel, Field, ValidationError

class User(BaseModel):
    # Define 'id' as an integer field with a description.
    id: int = Field(..., gt=0, description="An integer field for the user's ID")

    # Define 'name' as a string field with a description and a pattern.
    # The 'pattern' argument adds a validation rule that 'name' must only contain letters, numbers, and underscores.
    name: str = Field(..., pattern="^[A-Za-z0-9_]+$", description="A string field for the user's name")

    # Define 'age' as an integer field with a description.
    age: int = Field(..., gt=5, description="An integer field for the user's age")

    # Define 'is_active' as a boolean field with a description.
    is_active: bool = Field(..., description="A boolean field to represent if the user is active or not")

# Example data for creating User instances
user_data_too_young = {
    "id": 123,
    "name": "John Doe",
    "age": 4,
    "is_active": True
}

user_data_non_bool = {
    "id": 123,
    "name": "John Doe",
    "age": 5,
    "is_active": 'True'  # Non-boolean value for a boolean field
}

user_data_bad_string = {
    "id": 123,
    "name": "John Doe &&&",  # Invalid string not matching the pattern
    "age": 30,
    "is_active": True
}

user_data_valid = {
    "id": 123,
    "name": "John Doe",
    "age": 30,
    "is_active": True
}

users_data = [user_data_too_young, user_data_non_bool, user_data_bad_string, user_data_valid]

# Iterate over the example data and attempt to create User instances
for user_data in users_data:
    try:
        user = User(**user_data)

        # Print validated and parsed data if creation is successful
        print(user.id)
        print(user.name)
        print(user.age)
        print(user.is_active)
        print('---')

    # Catch and print any ValidationError
    except ValidationError as e:
        print(e)
