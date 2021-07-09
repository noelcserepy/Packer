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
    date = Column(DateTime)
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
    path = Column(String)
    date = Column(DateTime)
    preferred_filename = Column(String)
    texture_type = Column(String)
    channels = relationship("Channel", backref="texture")

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
        cascade="all, delete, delete-orphan",
    )

    def __repr__(self):
        return f"Packing Group: (name={self.identifier} | id={self.id} | status={self.status})"


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


engine = create_engine("sqlite:///db/packer.db", echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class DatabaseHandler:
    def __init__(self):
        self.date = datetime.now()

    def save_snapshot(self, snapshot):
        with Session() as session:
            self._add_new_snapshot_to_db(session, snapshot)

    def get_latest_snapshot(self):
        with Session() as session:
            snapshot = self._get_latest_snapshot_from_db(session)
            return snapshot.data

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

    def get_new_and_modified_packing_groups(self):
        with Session() as session:
            pgs = session.query(PackingGroup).filter(
                PackingGroup.status == "New" or PackingGroup.status == "Modified"
            )
            return pgs

    def populate_all_packing_groups(self, settings):
        with Session() as session:
            assets = session.query(Asset).all()
            self._make_packing_groups_from_assets(session, settings, assets)

    def populate_new_packing_groups(self, settings):
        with Session() as session:
            snapshot = self._get_latest_snapshot_from_db(session)
            assets = session.query(Asset).filter(Asset.date >= snapshot.date)
            self._make_packing_groups_from_assets(session, settings, assets)

    def set_packing_group_status(self, packing_group_id, status):
        with Session() as session:
            pg = session.get(PackingGroup, packing_group_id)
            pg.status = status
            session.commit()

    def _add_new_snapshot_to_db(self, session, snapshot):
        new_snapshot = Snapshot(date=self.date, data=snapshot)
        session.add(new_snapshot)
        session.commit()

    def _get_latest_snapshot_from_db(self, session):
        last_snapshot = session.query(Snapshot).order_by(desc(Snapshot.date)).first()
        return last_snapshot

    # Texture Functions
    def _add_new_texture_to_db(self, session, texture_match):
        existing_texture = self.get_texture(session, texture_match)
        if existing_texture:
            existing_asset = (
                session.query(Asset)
                .filter(Asset.id == existing_texture.asset_id)
                .first()
            )
            existing_asset.date = self.date
            existing_texture.date = self.date
        else:
            new_texture = self._make_new_texture(texture_match)
            self._match_new_texture_to_asset(session, new_texture)

    def _make_new_texture(self, texture_match):
        new_texture = Texture(
            asset_name=texture_match.asset_name,
            extension=texture_match.extension,
            directory=texture_match.directory,
            path=texture_match.path,
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
            matching_asset.date = self.date
        else:
            new_asset = Asset(
                name=new_texture.asset_name,
                directory=new_texture.directory,
                date=self.date,
            )
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
    def _make_packing_groups_from_assets(self, session, settings, assets):
        for asset in assets:
            for settings_packing_group in settings["packing_groups"]:
                existing_packing_group = (
                    session.query(PackingGroup)
                    .filter(
                        PackingGroup.asset_id == asset.id,
                        PackingGroup.identifier == settings_packing_group["identifier"],
                        PackingGroup.extension == settings_packing_group["extension"],
                    )
                    .first()
                )

                if existing_packing_group:
                    session.delete(existing_packing_group)
                    pg = PackingGroup(
                        identifier=settings_packing_group["identifier"],
                        extension=settings_packing_group["extension"],
                        asset_id=asset.id,
                        date=self.date,
                        status="Modified",
                    )
                else:
                    pg = PackingGroup(
                        identifier=settings_packing_group["identifier"],
                        extension=settings_packing_group["extension"],
                        asset_id=asset.id,
                        date=self.date,
                        status="New",
                    )

                    new_channels = self._make_new_channels(
                        settings_packing_group, asset
                    )
                    tt_count = len(settings_packing_group["texture_types"])
                    if not len(new_channels) == tt_count:
                        continue

                    for channel in new_channels:
                        pg.channels.append(channel)
                    session.add(pg)
                    session.commit()

    def _make_new_channels(self, settings_packing_group, asset):
        new_channels = []
        for tt in settings_packing_group["texture_types"]:
            for asset_tex in asset.textures:
                channel_texture = None
                if asset_tex.texture_type == tt:
                    channel_texture = asset_tex
                    break
            if not channel_texture:
                break

            new_channel = Channel(texture_type=tt, texture_id=channel_texture.id)
            new_channels.append(new_channel)
        return new_channels

    def _get_pgs_from_db(self, session):
        all_packing_groups = (
            session.query(PackingGroup)
            .options(subqueryload(PackingGroup.channels).subqueryload(Channel.texture))
            .all()
        )
        remade_pgs = []
        for pg in all_packing_groups:
            remade_pg = {
                "id": pg.id,
                "identifier": pg.identifier,
                "asset_name": pg.asset.name,
                "extension": pg.extension,
                "date": pg.date,
                "status": pg.status,
                "directory": pg.asset.directory,
                "channels": [
                    pg.channels[0],
                    pg.channels[1],
                    pg.channels[2],
                    pg.channels[3],
                ],
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

    def print_packing_groups(self):
        with Session() as session:
            for pg in session.query(PackingGroup).all():
                print(pg)
