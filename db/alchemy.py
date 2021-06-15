from datetime import datetime
from sqlalchemy import Integer, ForeignKey, String, Column, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


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
    scan_date = Column(String)
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
    name = Column(String)
    asset_id = Column(Integer, ForeignKey("asset.id"))
    textures = relationship(
        "Texture", secondary="texture_pg_link", back_populates="packing_groups"
    )

    def __repr__(self):
        return f"Packing Group: (name={self.name} | id={self.id})"


texture_pg_link = Table(
    "texture_pg_link",
    Base.metadata,
    Column("texture_id", Integer, ForeignKey("texture.id"), primary_key=True),
    Column(
        "packing_group_id", Integer, ForeignKey("packing_group.id"), primary_key=True
    ),
)


engine = create_engine("sqlite:///:memory:", echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class DatabaseHandler:
    def add_new_texture_to_db(self, texture_match):
        with Session() as session:
            new_texture = Texture(
                asset_name=texture_match.asset_name,
                extension=texture_match.extension,
                directory=texture_match.directory,
                scan_date=datetime.now().timestamp(),
                preferred_filename=texture_match.preferred_filename,
                texture_type=texture_match.texture_type,
            )

            asset = (
                session.query(Asset)
                .filter_by(name=new_texture.asset_name)
                .one_or_none()
            )

            if asset:
                new_texture.asset_id = asset.id
            else:
                new_asset = Asset(name=new_texture.asset_name)
                session.add(new_asset)
                session.commit()
                new_texture.asset_id = new_asset.id

            session.add(new_texture)
            session.commit()

    def add_textures_to_pg(self, packing_group):
        with Session() as session:
            textures_in_pg = session.query(Texture).filter(
                Texture.texture_type.in_(packing_group["group"])
            )

            for texture in textures_in_pg:
                pg_match = (
                    session.query(PackingGroup)
                    .filter(
                        PackingGroup.name == packing_group["identifier"],
                        PackingGroup.asset_id == texture.asset_id,
                    )
                    .one_or_none()
                )
                if pg_match:
                    pg_match.textures.append(texture)
                    session.commit()
                else:
                    new_pg = PackingGroup(
                        name=packing_group["identifier"], asset_id=texture.asset_id
                    )
                    new_pg.textures.append(texture)
                    session.commit()

    def print_assets(self):
        with Session() as session:
            for asset in session.query(Asset).all():
                print(asset)

    def print_textures(self):
        with Session() as session:
            for texture in session.query(Texture).all():
                print(texture)

    def get_packing_groups(self):
        with Session() as session:
            return session.query(PackingGroup).all()
