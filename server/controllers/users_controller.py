from ..models.user import User
from ..models import db

def get_all_users():
    users = db.session.query(User).all()
    print("USERS", users)
    return users


def get_a_single_user(id: int):
    user = db.session.query(User).filter(User.id == id).first()
    if user is None:
        print(f"User with ID {id} does not exist")
    print("USER", user)
    return user


def create_a_new_user(user):
    user_details = User(
        username=user.username,
        
        password=user.password
    )
    new_user = User.create(user_details)
    print("USER", new_user)
    return new_user


def update_user(id: int, user_obj):

    user = db.session.query(User).filter(User.id == id).first()

    if user is None:
        print(f"User with ID {id} does not exist")

    user["username"] = user_obj["username"]
    

    new_user_info = User.update(user)
    print("User", new_user_info)
    return new_user_info


def delete_user(id: int):

    user = db.session.query(User).filter(User.id == id).first()

    if user is None:
        print(f"User with ID {id} does not exist")

    User.delete(user)
    print(f"User with ID {id} has been deleted successfully")
    return True
