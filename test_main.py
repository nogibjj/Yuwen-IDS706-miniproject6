from main import create_connection, create_table, insert_user
from main import get_user_by_username, update_user_email, delete_user
from main import select_all_users, select_person_with_shortest_email
def test_insert_user():
    database_file = "test_database.db"
    connection = create_connection(database_file)
    create_table(connection)

    insert_user(connection, "AliceSmith", "alice@example.com")
    user = get_user_by_username(connection, "AliceSmith")
    connection.close()

    assert user is not None
    assert user[2] == "alice@example.com"

def test_update_user_email():
    database_file = "test_database.db"
    connection = create_connection(database_file)
    create_table(connection)

    insert_user(connection, "BobJohnson", "bob@example.com")
    update_user_email(connection, "BobJohnson", "new_email@example.com")
    user = get_user_by_username(connection, "BobJohnson")
    connection.close()

    assert user is not None
    assert user[2] == "new_email@example.com"

def test_delete_user():
    database_file = "test_database.db"
    connection = create_connection(database_file)
    create_table(connection)

    insert_user(connection, "CharlieBrown", "charlie@example.com")
    delete_user(connection, "CharlieBrown")
    user = get_user_by_username(connection, "CharlieBrown")
    connection.close()

    assert user is None

def test_select_person_with_shortest_email():
    database_file = "test_database.db"
    connection = create_connection(database_file)
    create_table(connection)

    # Insert users with different email lengths
    insert_user(connection, "AliceSmith", "alice@example.com")
    insert_user(connection, "BobJohnson", "b@example.com")
    insert_user(connection, "CharlieBrown", "charlie@example.com")

    person = select_person_with_shortest_email(connection)
    connection.close()

    assert person is not None
    assert person[1] == "BobJohnson"  # Assert the BobJohnson with the shortest email


def test_select_all_users():
    database_file = "new_full_database.db"
    connection = create_connection(database_file)
    create_table(connection)

    # Insert test users
    insert_user(connection, "AliceSmith", "alice@example.com")
    insert_user(connection, "BobJohnson", "bob@example.com")
    insert_user(connection, "CharlieBrown", "charlie@example.com")

    users = select_all_users(connection)
    connection.close()
    assert len(users) == 3  # Assert the number of retrieved users


if __name__ == "__main__":
    test_insert_user()
    test_update_user_email()
    test_delete_user()
    test_select_person_with_shortest_email()
    test_select_all_users()
