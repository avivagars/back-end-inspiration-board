from app.models.board import Board
from app.models.card import Card


def test_get_all_boards_no_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_boards_one_board(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1,
            "name": "Test Board",
            "owner": "Test Owner",
        }
    ]


def test_get_all_boards_one_board_three_cards(client, one_board_three_cards):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1,
            "name": "Test Board",
            "owner": "Test Owner",
        }
    ]


def test_post_new_board_empty_db(client):
    # Arrange
    new_board = {"name": "Test Name", "owner": "Test Owner"}

    # Act
    response = client.post("/boards", json=new_board)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == f"Board {new_board['name']} successfully created"


def test_post_new_board_no_name(client):
    # Arrange
    new_board = {"owner": "Test Owner"}

    # Act
    response = client.post("/boards", json=new_board)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details": "Invalid data"}


def test_post_new_board_no_owner(client):
    # Arrange
    new_board = {"name": "Test Name"}

    # Act
    response = client.post("/boards", json=new_board)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details": "Invalid data"}


def test_get_all_cards_one_board_no_cards(client, one_board):
    # Arrange
    board_id = Board.query.first().board_id

    # Act
    response = client.get(f"/boards/{board_id}/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_cards_one_board_three_cards(client, one_board_three_cards):
    # Arrange
    board_id = Board.query.first().board_id

    # Act
    response = client.get(f"/boards/{board_id}/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {"id": 1, "message": "Hello", "likes": 0},
        {"id": 2, "message": "Test", "likes": 1},
        {"id": 3, "message": "Goodbye", "likes": 2},
    ]


def test_update_likes_on_card(client, add_like):
    # Act
    response = client.put("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "message": "Updated Card Message",
        "likes": 6
    }


def test_add_like_card_not_found(client):
    # Act
    response = client.put("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "Message": "Card 1 not found"
    }
    assert Card.query.all() == []


def test_add_card_to_board(client, one_board):
    # Arrange
    new_card = {"message": "Test message"}

    # Act
    response = client.post("/boards/1/cards", json=new_card)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {'message': 'New card successfully created'}


def test_add_card_no_message(client, one_board):
    # Arrange
    new_card = {"test": 25}

    # Act
    response = client.post("/boards/1/cards", json=new_card)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details": "Invalid data"}


def test_delete_card(client, one_board_three_cards):
    # Arrange
    card_id = Card.query.first().card_id

    # Act
    response = client.delete(f"/cards/{card_id}")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        f"details": f'Card {card_id} successfully deleted'
    }


def test_delete_no_cards_card_not_found(client):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"Message": f"Card 1 not found"}
    assert Card.query.all() == []
