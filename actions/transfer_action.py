from enum import auto
from app import db
from sqlalchemy import inspect, MetaData, text
from sqlalchemy.ext.automap import automap_base
from models.transfer import Transfer

CREATE_STATEMENT = """
    CREATE TABLE IF NOT EXISTS transfer_{}(
        id SERIAL NOT NULL,
        sender VARCHAR(64) NOT NULL,
        receiver VARCHAR(64) NOT NULL,
        method VARCHAR(64) NOT NULL,
        total REAL NOT NULL,
        currency VARCHAR(64) NOT NULL,
        PRIMARY KEY(id)
    )
"""


def create_transfer_table(user_id: str):
    sql = text(CREATE_STATEMENT.format(user_id))
    with db.engine.connect() as conn:
        conn.execute(sql)
        return True


def transfer_money(
    sender_id: str, receiver_id: str, method: str, total: float, currency: str
):
    insp = inspect(db.engine)
    # Begin transactions
    create_transfer_table(sender_id)
    create_transfer_table(receiver_id)

    # Define two table in db
    Base = automap_base()
    Base.prepare(db.engine, reflect = True)
    SenderTable = Base.classes[f'transfer_{sender_id}']
    ReceiverTable = Base.classes[f'transfer_{receiver_id}']

    # Begin transaction
    db.session.begin()
    try:
        # First, check table with name (transfer_{receiver_id}, transfer_{sender_id}) is exists
        # If not, create new one
        if not insp.has_table(f"transfer_{sender_id}"):
            # TODO Create new table here
            pass
        if not insp.has_table(f"transfer_{receiver_id}"):
            # TODO Create new table here
            pass

        # Next, insert data to primary Transfer table
        trans = Transfer(
            sender=sender_id,
            receiver=receiver_id,
            currency=currency,
            total=total,
            method=method,
        )
        db.session.add(trans)
        # Insert to user transfer table (transfer_{receiver_id}, transfer_{sender_id})
        # 1. sender_table
        sender_trans = SenderTable(
            sender = sender_id,
            receiver = receiver_id,
            currency = currency,
            method = method,
            total = total
        )
        db.session.add(sender_trans)
        # 2. receiver_table
        receiver_trans = ReceiverTable(
            sender = sender_id,
            receiver = receiver_id,
            currency = currency,
            method = method,
            total = total
        )
        db.session.add(receiver_trans)

        # If there isn't error, commit the transaction
        db.session.commit()
    except Exception as e:
        print(e)
        # If there is an error, rollback
        db.session.rollback()

    return True
