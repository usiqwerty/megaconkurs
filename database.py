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


def append_entry(entry: ConcursPlace):
	global session
	new_record = ConcursPlaceSQL()
	for attr in dir(entry):
		if not attr.startswith('__'):
			if attr == "subjects":
				setattr(new_record, attr, str(getattr(entry, attr)))
			else:
				setattr(new_record, attr, getattr(entry, attr))
	session.add(new_record)
	session.commit()


def count_rows():
	try:
		return session.query(ConcursPlaceSQL.snils).count()
	except sqlalchemy.exc.ArgumentError:
		return 0


def find_all_by_snils(snils: int):
	DeclBase.metadata: MetaData
	tb:sqlalchemy.Table = DeclBase.metadata.tables["concurs"]

	query = select(tb).where(tb.c.snils == snils)

	return session.execute(query).fetchall()