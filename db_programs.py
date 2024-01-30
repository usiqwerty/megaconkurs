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
from concurs import ConcursPlace

DeclBase = declarative_base()
fn_database = "full_data.sqlite3"
engine = create_engine(f'sqlite:///{fn_database}')


class ConcursPlaceSQL(DeclBase):
	__tablename__ = 'concurs'
	id = Column(Integer, primary_key=True)
	position_number = Column("position_number", Integer)
	snils = Column("snils", Integer)
	bvi = Column("bvi", Boolean)
	prior = Column("prior", Integer)
	confirmed = Column("confirmed", Boolean)
	score = Column("score", Integer)
	degree = Column("degree", Integer)
	payment = Column("payment", Integer)
	subjects = Column("subjects", String)
	code = Column("code", String)
	vuz = Column("vuz", Integer)

	def __repr__(self):
		return f"SQL {self.position_number}@{self.code}: {self.snils} ({self.score}) p{self.prior} {'БВИ' if self.bvi else ''} {'ОРИГ' if self.confirmed else ''} {self.subjects}"


def start():
	global session

	DeclBase.metadata.create_all(engine)

	# Создаем фабрику для создания экземпляров Session. Для создания фабрики в аргументе
	# bind передаем объект engine
	Session = sessionmaker(bind=engine)

	# Создаем объект сессии из вышесозданной фабрики Session
	session = Session()


def sql_to_pyobj(sql_obj):
	pyobj = ConcursPlace()

	for attr in dir(pyobj):
		if not attr.startswith('__'):
			if attr == "other_programs":
				continue
			if attr == "subjects":
				setattr(pyobj, attr, str(getattr(sql_obj, attr)))
			else:
				setattr(pyobj, attr, getattr(sql_obj, attr))
	return pyobj


def pyobj_to_sql(pyobj):
	new_record = ConcursPlaceSQL()
	for attr in dir(pyobj):
		if not attr.startswith('__'):
			if attr == "other_programs":
				continue
			if attr == "subjects":
				setattr(new_record, attr, str(getattr(pyobj, attr)))
			else:
				setattr(new_record, attr, getattr(pyobj, attr))
	return new_record


def append_entry(entry: ConcursPlace):
	global session

	new_record = pyobj_to_sql(entry)
	session.add(new_record)
	session.commit()


def count_rows():
	try:
		return session.query(ConcursPlaceSQL.snils).count()
	except sqlalchemy.exc.ArgumentError:
		return 0


DeclBase.metadata: MetaData
tb: sqlalchemy.Table = DeclBase.metadata.tables["concurs"]


def find_all_by_snils(snils: int):
	query = select(tb).where(tb.c.snils == snils)

	res = session.query(ConcursPlaceSQL).from_statement(query)  # .execute(query).fetchall()
	if res:
		return [sql_to_pyobj(x) for x in res]
	else:
		return None


def find_all_by_program(program_code: str, vuz: str):
	"""Конкурсный список по коду программы"""
	query = select(tb).where(tb.c.code == program_code).where(tb.c.vuz == vuz)
	res = session.query(ConcursPlaceSQL).from_statement(query)  # .execute(query).fetchall()
	return [sql_to_pyobj(x) for x in res]


def find_all_by_program_extended(program_code: str, vuz: str):
	"""Конкурсный список по коду программы, подгружает другие заявления абитуриентов"""
	query = select(tb).where(tb.c.code == program_code).where(tb.c.vuz == vuz)
	res = session.query(ConcursPlaceSQL).from_statement(query)  # .execute(query).fetchall()

	result = []
	for x in res:
		abit = sql_to_pyobj(x)
		if abit.other_programs is None:
			abit.other_programs = find_all_by_snils(abit.snils)
		result.append(abit)
	return result


def get_all_programs_by_vuz(vuz):
	query = select(tb).where(tb.c.vuz == vuz)
	res = session.query(ConcursPlaceSQL.code).distinct()
	return [x[0] for x in res]
