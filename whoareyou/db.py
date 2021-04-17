# -*- coding: utf-8 -*-
import sqlalchemy
import sqlalchemy.ext.compiler
import sqlalchemy.ext.declarative
import sqlalchemy.sql.expression
import sqlalchemy.orm

engine = sqlalchemy.create_engine('sqlite:///contacts.sqlite', echo=True)
Base = sqlalchemy.ext.declarative.declarative_base(bind=engine)
Session = sqlalchemy.orm.sessionmaker(bind=engine)


@sqlalchemy.ext.compiler.compiles(sqlalchemy.sql.expression.Insert)
def _prefix_insert_with_ignore(insert, compiler, **kw):
    """
    A compiler extension to always replace `INSERT` by `INSERT OR IGNORE`.

    See <https://stackoverflow.com/a/61153835/1257318>.
    """
    return compiler.visit_insert(insert.prefix_with('OR IGNORE'), **kw)
