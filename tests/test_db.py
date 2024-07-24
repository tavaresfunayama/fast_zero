from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='funay', email='funay@mail.com', password='senha')
    session.add(user)
    session.commit()
    result = session.scalar(select(User).where(User.email == 'funay@mail.com'))

    assert result.username == 'funay'
