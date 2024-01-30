"""
	This file is part of megaconcurs.

	megaconcurs is free software: you can redistribute it and/or modify it under the terms of the
	GNU General Public License as published by the Free Software Foundation, either version 2 of the License,
	or (at your option) any later version.

	megaconcurs is distributed in the hope that it will be useful, but WITHOUT ANY
	WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
	General Public License for more details.

	You should have received a copy of the GNU General Public License along with
	Foobar. If not, see <https://www.gnu.org/licenses/>.
"""

import sqlalchemy.orm
from sqlalchemy import create_engine, Column, Integer, String, Boolean, MetaData
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

session: sqlalchemy.orm.Session
meta: MetaData

DeclBase = declarative_base()
fn_database = "vuzes.sqlite3"
engine = create_engine(f'sqlite:///{fn_database}')


class VuzSQL(DeclBase):
	__tablename__ = 'vuzes'
	id = Column(Integer, primary_key=True)
	shortname = Column("shortname", String)
	code = Column("code", String)
	fullname = Column("fullname", String)
	description = Column("description", String)

	def __repr__(self):
		return f"SQL {self.shortname}({self.code}): {self.fullname} "


def start():
	global session

	DeclBase.metadata.create_all(engine)

	# Создаем фабрику для создания экземпляров Session. Для создания фабрики в аргументе
	# bind передаем объект engine
	Session = sessionmaker(bind=engine)

	# Создаем объект сессии из вышесозданной фабрики Session
	session = Session()


def append_entry(short, code, fullname, descr):
	global session

	new_record = VuzSQL()
	new_record.code = code
	new_record.shortname = short
	new_record.fullname = fullname
	new_record.description = descr
	session.add(new_record)
	session.commit()


def count_rows():
	try:
		return session.query(VuzSQL).count()
	except sqlalchemy.exc.ArgumentError:
		return 0

def get_all_vuzes():
	query=session.query(VuzSQL)
	return query
def get_vuz_info(vuz_code: str):
	query = select(VuzSQL).where(tb.c.code == vuz_code)
	return session.execute(query).first()
DeclBase.metadata: MetaData
tb: sqlalchemy.Table = DeclBase.metadata.tables["vuzes"]

