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
from sqlalchemy.ext.orderinglist import ordering_list


Base = declarative_base()


class Asset(Base):
    __tablename__ = "asset"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    directory = Column(String)
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
    channels = relationship(
        "Channel",
        order_by="Channel.position",
        collection_class=ordering_list("position"),
    )
    all_textures = relationship(
        "Texture", secondary="texture_pg_link", back_populates="packing_groups" #maybe obsolete
    )

    def __repr__(self):
        return f"Packing Group: (name={self.identifier} | id={self.id})"


class Channel(Base):
    __tablename__ = "channel"
    id = Column(Integer, primary_key=True)
    packing_group_id = Column(Integer, ForeignKey("packing_group.id"))
    texture_id = Column(Integer, ForeignKey("texture.id"))
    position = Column(Integer)
    texture_type = Column(String)


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
    def __init__(self):
        self.date = datetime.now()

    def save_snapshot(self, snapshot):
        with Session() as session:
            self._add_new_snapshot_to_db(session, snapshot)

    def get_last_snapshot(self):
        with Session() as session:
            return self._get_last_snapshot_from_db(session)

    def add_texture(self, texture_match):
        with Session() as session:
            self._add_new_texture_to_db(session, texture_match)

    def get_all_packing_groups(self):
        with Session() as session:
            all_pgs = self._get_pgs_from_db(session)
        return all_pgs

    def get_all_packing_groups_ordered(self):
        with Session() as session:
            pg_info = (
                session.query(PackingGroup, Asset)
                .join(Asset)
                .order_by(Asset.name)
                .all()
            )
            return pg_info

    def populate_packing_groups(self, settings):
        with Session() as session:
            self._match_textures_to_pg(session, settings)

    def _add_new_snapshot_to_db(self, session, snapshot):
        new_snapshot = Snapshot(date=self.date, data=snapshot)
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
            date=self.date,
            preferred_filename=texture_match.preferred_filename,
            texture_type=texture_match.texture_type,
        )
        return new_texture

    def _match_new_texture_to_asset(self, session, new_texture):
        matching_asset = (
            session.query(Asset)
            .filter(Asset.name == new_texture.asset_name)
            .one_or_none()
        )
        if matching_asset:
            new_texture.asset_id = matching_asset.id
        else:
            new_asset = Asset(name=new_texture.asset_name, directory=new_texture.directory)
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

    def get_all_textures(self, session):
        texture_query = session.query(Texture).all()
        return texture_query

    # Packing Group Functions
    def _match_textures_to_pg(self, session, settings):
        all_assets = session.query(Asset).all()
        for asset in all_assets:
            for texture in asset.textures:
                print(texture.preferred_filename)
        for asset in all_assets:
            for settings_packing_group in settings["packing_groups"]:
                new_pg = PackingGroup(
                    identifier=settings_packing_group["identifier"],
                    extension=settings_packing_group["extension"],
                    asset_id=asset.id,
                    date=self.date,
                    status="Ready",
                )

                new_channels = []
                for tt in settings_packing_group["texture_types"]:
                    for asset_tex in asset.textures:
                        channel_texture = None
                        if asset_tex.texture_type == tt:
                            channel_texture = asset_tex
                            break
                    if not channel_texture:
                        break

                    new_channel = Channel(
                        texture_type=tt,
                        texture_id=channel_texture.id
                    )
                    new_channels.append(new_channel)

                if not len(new_channels) == len(settings_packing_group["texture_types"]):
                    continue
            
                for channel in new_channels:
                    new_pg.channels.append(channel)
                session.add(new_pg)
                session.commit()


        pgs = session.query(PackingGroup).all()
        for pg in pgs:
            print(pg.identifier, pg.asset.name)
            for c in pg.channels:
                print(c.texture_type, c.texture_id)



    def _get_pgs_from_db(self, session):
        all_packing_groups = session.query(PackingGroup).all()
        remade_pgs = []
        for pg in all_packing_groups:
            remade_pg = {
                "identifier": pg.identifier,
                "asset_name": pg.asset.name,
                "extension": pg.extension,
                "date": pg.date,
                "status": pg.status,
                "directory": pg.asset.directory
            }
            remade_pgs.append(remade_pg)
        return remade_pgs

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
