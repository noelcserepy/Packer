from datetime import datetime
from typing import Text
from sqlalchemy import (
    Integer,
    ForeignKey,
    String,
    Column,
    Table,
    create_engine,
    inspect,
    desc,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, subqueryload
from sqlalchemy.sql.selectable import subquery
from sqlalchemy.sql.sqltypes import DateTime, PickleType


Base = declarative_base()


class Asset(Base):
    __tablename__ = "asset"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    textures = relationship("Texture", backref="asset")
    packing_groups = relationship("PackingGroup", backref="asset")

    def __repr__(self):
        return f"Asset: (asset_id={self.id} | name={self.name})"


class Texture(Base):
    __tablename__ = "texture"
    id = Column(Integer, primary_key=True)
    asset_name = Column(String)
    asset_id = Column(Integer, ForeignKey("asset.id"))
    extension = Column(String)
    directory = Column(String)
    date = Column(DateTime)
    preferred_filename = Column(String)
    texture_type = Column(String)
    packing_groups = relationship(
        "PackingGroup", secondary="texture_pg_link", back_populates="textures"
    )

    def __repr__(self):
        return f"Texture: (asset_id={self.asset_id} | asset_name={self.asset_name} | texture_type={self.texture_type})"


class PackingGroup(Base):
    __tablename__ = "packing_group"
    id = Column(Integer, primary_key=True)
    identifier = Column(String)
    extension = Column(String)
    asset_id = Column(Integer, ForeignKey("asset.id"))
    date = Column(DateTime)
    status = Column(String)
    textures = relationship(
        "Texture", secondary="texture_pg_link", back_populates="packing_groups"
    )

    def __repr__(self):
        return f"Packing Group: (name={self.identifier} | id={self.id})"


class Snapshot(Base):
    __tablename__ = "snapshot"
    id = Column(Integer, primary_key=True)
    data = Column(PickleType)
    date = Column(DateTime)

    def __repr__(self):
        return f"Snapshot: (id={self.id} | date={self.date})"


texture_pg_link = Table(
    "texture_pg_link",
    Base.metadata,
    Column("texture_id", Integer, ForeignKey("texture.id"), primary_key=True),
    Column(
        "packing_group_id", Integer, ForeignKey("packing_group.id"), primary_key=True
    ),
)


engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class DatabaseHandler:
    def save_snapshot(self, snapshot):
        with Session() as session:
            self._add_new_snapshot_to_db(session, snapshot)

    def get_last_snapshot(self):
        with Session() as session:
            return self._get_last_snapshot_from_db(session)

    def add_texture(self, texture_match):
        with Session() as session:
            self._add_new_texture_to_db(session, texture_match)

    def populate_packing_groups(self, packing_group):
        with Session() as session:
            self._add_textures_to_pg(session, packing_group)

    def get_all_packing_groups(self):
        with Session() as session:
            return self._get_pgs_from_db(session)

    def get_all_packing_groups_ordered(self):
        with Session() as session:
            pg_info = (
                session.query(PackingGroup, Asset)
                .join(Asset)
                .order_by(Asset.name)
                .all()
            )
            return pg_info


    # Snapshot Functions
    def _add_new_snapshot_to_db(self, session, snapshot):
        new_snapshot = Snapshot(date=datetime.now(), data=snapshot)
        session.add(new_snapshot)
        session.commit()

    def _get_last_snapshot_from_db(self, session):
        last_snapshot = session.query(Snapshot).order_by(desc(Snapshot.date)).first()
        print(last_snapshot.date)
        return last_snapshot.data

    # Texture Functions
    def _add_new_texture_to_db(self, session, texture_match):
        existing_texture = self.get_texture(session, texture_match)
        if not existing_texture:
            new_texture = self._make_new_texture(texture_match)
            self._match_new_texture_to_asset(session, new_texture)

    def _make_new_texture(self, texture_match):
        new_texture = Texture(
            asset_name=texture_match.asset_name,
            extension=texture_match.extension,
            directory=texture_match.directory,
            date=datetime.now(),
            preferred_filename=texture_match.preferred_filename,
            texture_type=texture_match.texture_type,
        )
        return new_texture        

    def _match_new_texture_to_asset(self, session, new_texture):
        matching_asset = (
            session.query(Asset).filter(Asset.name == new_texture.asset_name).one_or_none()
        )
        if matching_asset:
            new_texture.asset_id = matching_asset.id
        else:
            new_asset = Asset(name=new_texture.asset_name)
            session.add(new_asset)
            session.commit()
            new_texture.asset_id = new_asset.id

        session.add(new_texture)
        session.commit()

    def get_texture(self, session, texture):
        texture_query = (
            session.query(Texture)
            .filter(
                Texture.preferred_filename == texture.preferred_filename,
                Texture.directory == texture.directory,
            )
            .one_or_none()
        )
        return texture_query

    # Packing Group Functions
    def _add_textures_to_pg(self, session, packing_group):
        textures_in_pg = session.query(Texture).filter(
            Texture.texture_type.in_(packing_group["group"])
        )
        self._match_textures_to_pg(textures_in_pg, session, packing_group)

    def _match_textures_to_pg(self, textures_in_pg, session, packing_group):
        for texture in textures_in_pg:
            pg_match = (
                session.query(PackingGroup)
                .filter(
                    PackingGroup.identifier == packing_group["identifier"],
                    PackingGroup.asset_id == texture.asset_id,
                )
                .one_or_none()
            )
            if pg_match:
                pg_match.textures.append(texture)
                session.commit()
            else:
                self._add_new_pg_to_db(packing_group, texture, session)

    def _add_new_pg_to_db(self, packing_group, texture, session):
        new_pg = PackingGroup(
            identifier=packing_group["identifier"],
            extension=packing_group["extension"],
            asset_id=texture.asset_id,
            date=datetime.now(),
            status="Ready",
        )
        new_pg.textures.append(texture)
        session.commit()

    def _get_pgs_from_db(self, session):
        all_packing_groups = session.query(PackingGroup).all()
        for item in all_packing_groups:
            print(item.textures)
        return all_packing_groups

    # Printing Functions
    def print_assets(self):
        with Session() as session:
            for asset in session.query(Asset).all():
                print(asset)

    def print_textures(self):
        with Session() as session:
            for texture in session.query(Texture).all():
                print(texture)

    def print_snapshots(self):
        with Session() as session:
            for snapshot in session.query(Snapshot).all():
                print(snapshot)

