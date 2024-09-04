from snowflake.snowpark import Session
def fetch_session():
    session = Session.builder.config("connection_name", "datacrawlerconn").create()
    return session
