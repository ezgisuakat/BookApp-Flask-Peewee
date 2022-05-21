from flask import Flask, request, render_template, url_for, redirect
from peewee import *


app = Flask(__name__, template_folder='templates')


db = SqliteDatabase('Book.db')



class Book(Model):
   id = IntegerField(primary_key=True)
   name_of_book = CharField()
   name_of_writer = CharField()
   class Meta:
      database = db
      db_table = 'Book'






@app.route("/", methods = ['GET', 'POST'])
def home():

    return  render_template("home.html")




@app.route('/show', methods=['GET'])
def show():

    list_of_data = []
    rows = Book.select()
    print(type(rows))
    for row in rows:
        new = {'id': row.id, "name_of_book": row.name_of_book, "name_of_writer": row.name_of_writer}
        list_of_data.append(new)

    print(list_of_data)

    return  render_template("show.html",  list_of_data = list_of_data)




@app.route('/add', methods=['POST'])
def add():
    book = request.form.get("book")
    writer = request.form.get("writer")

    if book == ""  and  writer == "" :

        return redirect(url_for("home"))

    new_book = Book(name_of_book=book, name_of_writer=writer)
    new_book.save()

    return redirect(url_for("home"))


@app.route('/delete/<string:id>')
def delete(id):
    qry = Book.delete().where(Book.id == id)
    qry.execute()

    return redirect(url_for("show"))



@app.route('/update/<string:id>',  methods = ['GET', 'POST'])
def update(id):
    id = int(id)
    new_book = request.form.get("new_book")
    new_writer = request.form.get("new_writer")
    print(f"new book : {new_book}")
    print(f"new writer : {new_writer}")

    row = Book.get(Book.id == int(id))
    print("name of book: {} name of writer: {}".format(row.name_of_book, row.name_of_writer))
    row.name_of_book =  new_book
    print(row.name_of_book)
    row.name_of_writer = new_writer
    print(row.name_of_writer)
  #  row.save()

    return render_template("update.html")




#UPDATE
"""

1_
    nrows = Book.update(name_of_book=new_book, name_of_writer=new_writer).where(Book.id).execute()
    nrows.execute()

"""
"""
2_
    #new_qry_book = Book.update({Book[id].name_of_book : new_book}).where(Book.id == int(id))
    #new_qry_book.execute()
    #new_qry_writer = Book.update({Book[id].name_of_writer : new_writer}).where(Book.id == int(id))
    #new_qry_writer.execute()


"""
"""
3_
    row = Book.get(Book.id == int(id))
    print("name of book: {} name of writer: {}".format(row.name_of_book, row.name_of_writer))
    row.name_of_book =  new_book
    print(row.name_of_book)
    row.name_of_writer = new_writer
    print(row.name_of_writer)
    row.save()
"""
""" 
4_
    #rows = Book.select()
    # rows[int(id)].name_of_book = new_book
    # rows[int(id)].name_of_writer = new_writer
    #Book.bulk_update([rows[int(id)]], fields=[Book.name_of_book])
    #Book.bulk_update([rows[int(id)]], fields=[Book.name_of_writer])
    
"""
"""
5_
    q1 = Book.update(name_of_book = new_book).where(Book.id == int(id))
    q1.execute()
    q2 = Book.update(name_of_writer = new_writer).where(Book.id == int(id))
    q2.execute()

"""




if __name__ == "__main__":
    Book.create_table()
    app.run(debug=True)