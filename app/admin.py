from sqladmin import Admin


def setup_admin(app, engine) -> Admin:
    admin = Admin(app, engine, title="Books Admin")
    return admin
