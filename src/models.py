from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    #-- RELACIONES --
    # Uno a muchos, accede a todos los posts de un usuario con user.posts
    posts = relationship("Post", back_populates="author")

    # Uno a muchos, accede a todos los comentarios de un usuario con user.comments
    comments = relationship("Comment", back_populates="author")

    # Uno a muchos, accede a todos los followers de un usuario con user.following
    following = relationship("Follower", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id")) # Clave foránea hacia User
    photo_url: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str] = mapped_column(Text, nullable=True)

    #-- RELACIONES (Más info en la primera class)--
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "photo_url": self.photo_url,
            "caption": self.caption,
        }
    

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id")) # Clave foránea hacia User
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id")) # Clave foránea hacia Post 
    text: Mapped[str] = mapped_column(Text, nullable=False)

    #-- RELACIONES (Más info en la primera class)--
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "text": self.text,
        }


class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    you_follow: Mapped[int] = mapped_column(ForeignKey("user.id")) # Clave foránea hacia User
    follows_you: Mapped[int] = mapped_column(ForeignKey("user.id")) # Clave foránea hacia User

    def serialize(self):
        return {
            "id": self.id,
            "you_follow": self.you_follow,
            "follows_you": self.follows_you,
        }