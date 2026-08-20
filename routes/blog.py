"""Blog routes: posts, comments, file uploads."""

import os

from flask import Blueprint, request, jsonify, render_template, send_file

from models import db, Post, Comment

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/posts")
def list_posts():
    posts = Post.query.all()
    return jsonify([{"id": p.id, "title": p.title, "body": p.body} for p in posts])


@blog_bp.route("/posts/<int:post_id>")
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "not found"}), 404
    comments = Comment.query.filter_by(post_id=post_id).all()
    # Renders user-supplied content; templates use |safe in index.html
    return render_template(
        "index.html", post=post, comments=[c.body for c in comments]
    )


@blog_bp.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json() or {}
    # Anyone can post as anyone: no ownership/auth check
    post = Post(
        user_id=data.get("user_id"),
        title=data.get("title", ""),
        body=data.get("body", ""),
    )
    db.session.add(post)
    db.session.commit()
    return jsonify({"id": post.id}), 201


@blog_bp.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    # No permission check: any user can delete any post
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
    return jsonify({"ok": True})


@blog_bp.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f:
        return jsonify({"error": "no file"}), 400

    # Original filename used directly: path traversal
    dest = os.path.join("/tmp/uploads", f.filename)
    f.save(dest)
    return jsonify({"saved": dest})


@blog_bp.route("/download")
def download():
    name = request.args.get("name")
    # Arbitrary file read from the server
    return send_file(name, as_attachment=True)


@blog_bp.route("/posts/<int:post_id>/comments", methods=["POST"])
def add_comment(post_id):
    data = request.get_json() or {}
    comment = Comment(post_id=post_id, user_id=data.get("user_id"), body=data.get("body", ""))
    db.session.add(comment)
    db.session.commit()
    return jsonify({"id": comment.id}), 201
