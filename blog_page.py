from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
 
app = Flask(__name__)
app.secret_key = "secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/blog_page'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

db = SQLAlchemy(app)

class Blog_page(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    text = db.Column(db.String(1500), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime())
    image_url = db.Column(db.String(1024))

    def __init__(self, text):
        self.text = text
        self.created_at = datetime.datetime.now()
        self.updated_at = self.created_at;

def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    id = request.form['id']
    file = request.files['data']
    filename = request.form['filename']
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], id + filename)
    file.save(filepath)
    entry = Blog_page.query.get(id)
    entry.image_url = filepath
    db.session.commit()

    return jsonify({"message": "success"}), 200  

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/blog')
def list_post():
    blog = Blog_page.query.order_by(Blog_page.id.desc())
    return render_template('main.html', blog=blog)

from flask import jsonify, request
@app.route('/blog', methods=['POST'])
def add_post():

    blog_data = request.form
    text = blog_data['text']

    if text == "":
        return jsonify({"message": "failed!"}), 400
    else:
        blog = Blog_page(text=text)
        db.session.add(blog)
        db.session.commit()
        return jsonify({"message": "success!", "id": blog.id, "created_at": blog.created_at, "updated_at": blog.updated_at}), 200


@app.route('/blog/<int:id>', methods=['DELETE'])
def delete_entry(id):
    blog=Blog_page.query.get(id)
    if blog.image_url:
        filename = os.path.join(app.root_path, blog.image_url)
        os.remove(filename)
    db.session.delete(blog)
    db.session.commit()
    return jsonify({"message": "success!"}), 200

@app.route('/blog/<int:id>', methods=['PUT'])
def edit_entry(id):
    blog_data = request.form
    updated_text = blog_data['text']
    if updated_text == "":
        return jsonify({"message": "failed!"}), 400
    else:
        blog = Blog_page.query.get(id)
        blog.text = updated_text
        blog.updated_at = datetime.datetime.now()
        db.session.commit()
        return jsonify({"message": "success!", "updated_at": blog.updated_at}), 200




if __name__ == '__main__':                             
   app.run(debug=True) 








# *   *   *   *   *   * #########################################################
#   *   *   *   *   *   #########################################################
# *   *   *   *   *   *
#   *   *   *   *   *   #########################################################
# *   *   *   *   *   * #########################################################
#   *   *   *   *   *
# *   *   *   *   *   * #########################################################
#   *   *   *   *   *   #########################################################
# *   *   *   *   *   *
#################################################################################
#################################################################################

#################################################################################
#################################################################################

#################################################################################
#################################################################################

#################################################################################
#################################################################################







#
#
#
#
#
#                                   *
#                       *          * *          *
#             *        * *        * * *        * *        *
#     *      * *      * * *      * * * *      * * *      * *      *
#    * *    * * *    * * * *    * * * * *    * * * *    * * *    * *
#   * * *  * * * *  * * * * *  * * * * * *  * * * * *  * * * *  * * * 

















