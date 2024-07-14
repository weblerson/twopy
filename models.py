from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, relationship

from sqlalchemy import Integer, String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column

from typing import List

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

candidatos_vagas_association = Table(
    'candidatos_vagas', Base.metadata,
    Column('candidato_id', ForeignKey('candidatos.id'), primary_key=True),
    Column('vaga_id', ForeignKey('vagas.id'), primary_key=True)
)


class Candidatos(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50))
    endereco: Mapped[str] = mapped_column(String(100))

    vagas: Mapped[List["Vagas"]] = relationship(
        secondary=candidatos_vagas_association,
        back_populates="candidatos"
    )

class Recrutadores(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50))
    cnpj_id: Mapped[int] = mapped_column(ForeignKey('empresa.id'), unique=True) # Relacionamento com a tabela empresa

    empresa: Mapped["Empresa"] = relationship(back_populates="recrutador") 

class Empresa(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(30))
    funcao: Mapped[str] = mapped_column(String(80))
    cnpj: Mapped[str] = mapped_column(String(50))

    recrutador: Mapped[List["Recrutadores"]] = relationship(
        uselist=False,
        back_populates="empresa"
    )

    vagas: Mapped[List["Vagas"]] = relationship(
        back_populates="empresa",
        cascade="all, delete-orphan"
    )

class Vagas(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))
    cnpj_id: Mapped[int] =  mapped_column(ForeignKey('empresa.id'))# Relacionamento com a tabela empresa

    empresa: Mapped["Empresa"] = relationship(
        back_populates="vagas"
    )

    candidatos: Mapped[List["Candidatos"]] = relationship(
        "Candidatos",
        secondary=candidatos_vagas_association,
        back_populates="vagas"
    )

class Aplicacoes(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    candidato_id: Mapped[int] = mapped_column(ForeignKey('candidatos.id'))
    vaga_id: Mapped[int] = mapped_column(ForeignKey('vagas.id'))
    
    candidato: Mapped["Candidatos"] = relationship("Candidatos")
    vaga: Mapped["Vagas"] = relationship("Vagas")


