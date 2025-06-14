# -*- coding: utf-8 -*-
from src.models.user import db 
from sqlalchemy.orm import backref

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    laws = db.relationship("Law", backref="subject", lazy=True, foreign_keys='Law.subject_id')

    def __repr__(self):
        return f"<Subject {self.name}>"

class Law(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    content = db.Column(db.Text, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=True)
    audio_url = db.Column(db.String(500), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('law.id'), nullable=True)

    # =====================================================================
    # <<< INÍCIO DA IMPLEMENTAÇÃO: NOVO CAMPO NO MODELO >>>
    # =====================================================================
    juridiques_explanation = db.Column(db.Text, nullable=True)
    # =====================================================================
    # <<< FIM DA IMPLEMENTAÇÃO: NOVO CAMPO NO MODELO >>>
    # =====================================================================

    # =====================================================================
    # <<< INÍCIO DA CORREÇÃO DEFINITIVA >>>
    # O parâmetro 'lazy="dynamic"' foi REMOVIDO da relação abaixo.
    # Esta é a principal correção que resolve o conflito.
    # =====================================================================
    children = db.relationship('Law', 
                               backref=backref('parent', remote_side=[id]),
                               cascade="all, delete-orphan")
    # =====================================================================
    # <<< FIM DA CORREÇÃO DEFINITIVA >>>
    # =====================================================================

    useful_links = db.relationship('UsefulLink', back_populates='law', lazy="dynamic", cascade="all, delete-orphan")

    # =====================================================================
    # <<< INÍCIO DA NOVA FUNCIONALIDADE: RELAÇÃO COM O BANNER >>>
    # =====================================================================
    # 'uselist=False' cria uma relação um-para-um (cada lei só pode ter um banner).
    # 'cascade="all, delete-orphan"' garante que se a lei for deletada, o banner associado também será.
    banner = db.relationship('LawBanner', backref='law', uselist=False, cascade="all, delete-orphan")
    # =====================================================================
    # <<< FIM DA NOVA FUNCIONALIDADE >>>
    # =====================================================================


    def __repr__(self):
        audio_indicator = " (Audio)" if self.audio_url else ""
        return f"<Law {self.title}{audio_indicator}>"

class UsefulLink(db.Model):
    __tablename__ = 'useful_link'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    law_id = db.Column(db.Integer, db.ForeignKey('law.id'), nullable=False)
    law = db.relationship('Law', back_populates='useful_links')

    def __repr__(self):
        return f'<UsefulLink {self.title}>'
