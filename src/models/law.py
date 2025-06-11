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
    # <<< INÍCIO: IMPLEMENTAÇÃO "ENTENDENDO O JURIDIQUÊS" >>>
    # Adicionamos a relação para os termos jurídicos.
    # =====================================================================
    juridiques_terms = db.relationship('JuridiquesTerm', back_populates='law', lazy="dynamic", cascade="all, delete-orphan")
    # =====================================================================
    # <<< FIM: IMPLEMENTAÇÃO "ENTENDENDO O JURIDIQUÊS" >>>
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

# =====================================================================
# <<< INÍCIO: IMPLEMENTAÇÃO "ENTENDENDO O JURIDIQUÊS" >>>
# Criamos um novo modelo para armazenar os termos e suas definições.
# =====================================================================
class JuridiquesTerm(db.Model):
    __tablename__ = 'juridiques_term'
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(200), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    law_id = db.Column(db.Integer, db.ForeignKey('law.id'), nullable=False)
    law = db.relationship('Law', back_populates='juridiques_terms')

    def __repr__(self):
        return f'<JuridiquesTerm {self.term}>'
# =====================================================================
# <<< FIM: IMPLEMENTAÇÃO "ENTENDENDO O JURIDIQUÊS" >>>
# =====================================================================
