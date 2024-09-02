from snowflake.snowpark import Session
def fetch_session():
    session = Session.builder.config("connection_name", "catalogpocconn").create()
    return session