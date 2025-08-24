from datetime import timedelta

import requests
from flask import flash, json, redirect, render_template, request, session, url_for
from mongoengine.errors import DoesNotExist

from app import app

from .controllers import (
    LoginForm,
    SignupForm,
    admin_login,
    flash_errors,
    is_logout,
    login_required,
)
from .models import Book, Member, Transaction


@app.route("/")
def home():
    return render_template("home.html", active_home=True)


@app.errorhandler(404)
def invalid_route():
    return render_template("404.html"), 404


@app.route("/login", methods=("GET", "POST"))
@is_logout
def login():
    form = LoginForm()

    if request.method == "POST":
        # ========== Form Validation ===========
        app.logger.debug("validate? %s", form.validate())
        app.logger.debug("errors: %s %s", form.email.errors, form.password.errors)

        if form.validate():
            app.logger.debug("Valid form data, proceeding with login")
            # ==========  User validation =============
            form_email = form.email.data
            form_email = form_email.lower()
            form_password = form.password.data
            form_checkbox = form.checkbox.data

            try:
                user = Member.objects.get(email=form_email)
                if user.check_password(form_password):
                    flash("Successfully logged-in", "success")

                    session.permanent = True
                    if form_checkbox:
                        app.permanent_session_lifetime = timedelta(hours=5)
                    else:
                        app.permanent_session_lifetime = timedelta(hours=1)
                    session["user"] = user
                    session["logged_in"] = True

                    return redirect("/member/" + session["user"]["username"])

                else:
                    flash("Password is incorrect", "danger")
                    return redirect(url_for("login"))
            except DoesNotExist:
                flash("Email not registered!!", "danger")
                return redirect(url_for("signup"))

        else:
            app.logger.debug("Invalid form data")
            if form.email.data == "":
                flash("Email is required", "danger")
            else:
                flash_errors(form)
            return redirect(url_for("login"))

    return render_template("login.html", form=form, active_login=True)


@app.route("/signup", methods=["GET", "POST"])
@is_logout
def signup():
    form = SignupForm()
    if request.method == "POST":
        # ========== Form Validation ===========
        app.logger.debug("validate? %s", form.validate())
        app.logger.debug("errors: %s %s", form.email.errors, form.password.errors)

        if form.validate():
            app.logger.debug("Valid form data, proceeding with signup")
            # ==========  User validation =============
            form_name = form.name.data
            form_email = form.email.data
            form_email = form_email.lower()
            form_username = form.username.data
            form_password = form.password.data

            try:
                Member.objects.get(email=form_email)

                flash("Email already registered!!", "danger")
                # return redirect( url_for('signup') )
            except DoesNotExist:
                try:
                    Member.objects.get(username=form_username)
                    flash("Username already registered!!", "danger")
                    # return redirect( url_for('signup') )

                except DoesNotExist:
                    user = Member(
                        name=form_name,
                        email=form_email,
                        password=form_password,
                        username=form_username,
                        admin=False,
                        active=False,
                    )
                    user.set_password(form_password)
                    user.save()
                    flash("Account created Successfully", "success")
                    return redirect(url_for("login"))

            # return redirect( url_for('signup') )

        else:
            app.logger.debug("Invalid form data")
            if form.name.data == "":
                flash("Name is required", "danger")
                app.logger.debug("Name is required")
            elif form.email.data == "":
                flash("Email is required", "danger")
                app.logger.debug("Email is required")
            else:
                flash_errors(form)
                app.logger.debug("Form errors: %s", form.errors)

    return render_template("signup.html", form=form, active_signup=True)


@app.route("/logout")
@login_required
def logout():
    session.pop("user", None)
    session.pop("logged_in", None)
    flash("Successfully Logged out", "success")
    return redirect(url_for("home"))


@app.route("/dashboard/")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/add-book", methods=["GET", "POST"])
@admin_login
def add_book():
    if request.method == "POST":
        request.form.get("title")
        request.form.get("author")
        request.form.get("isbn")
        request.form.get("publisher")
        request.form.get("page")

        frappe_api_url = "https://frappe.io/api/method/frappe-library?"

        for key, value in request.form.items():
            if value:
                frappe_api_url = frappe_api_url + key + "=" + value + "&"
        request_url = frappe_api_url[:-1]

        print(request_url)
        books_req = requests.get(request_url).json()
        books_data = books_req.get("message")
        app.logger.debug("Books data from API: %s", books_data)
        for book in books_data:
            db_book = Book.objects(bookID=(book["bookID"]))
            app.logger.debug("Database book check: %s", db_book)
            if len(db_book) == 0:
                new_book = Book(
                    bookID=book["bookID"],
                    title=book["title"],
                    authors=book["authors"],
                    average_rating=book["average_rating"],
                    isbn=book["isbn"],
                    isbn13=book["isbn13"],
                    language_code=book["language_code"],
                    num_pages=book["num_pages"],
                    ratings_count=book["ratings_count"],
                    text_reviews_count=book["text_reviews_count"],
                    publication_date=book["publication_date"],
                    publisher=book["publisher"],
                )
                # print(new_book)
                new_book.save()
                flash("book added successfully", "success")
            else:
                flash("Book Already Exist", "danger")

    return render_template("add-book.html", active_add_book=True)


@app.route("/books")
def books():
    books = Book.objects()
    members = Member.objects()

    return render_template(
        "books2.html", books=books, members=members, active_books=True
    )


@app.route("/members")
@admin_login
def members():
    members = Member.objects()

    return render_template("members.html", members=members, active_members=True)


@app.route("/member/<username>")
@login_required
def member(username):
    member = Member.objects(username=username)
    app.logger.debug("Fetched member: %s", member)
    if len(member) > 0:
        member = member[0]
        if not session["user"]["admin"]:
            if member["username"] == session["user"]["username"]:
                pass
            else:
                flash("You don't have permission to perform this action", "danger")
                return redirect("/member/" + session["user"]["username"])

    return render_template("member.html", member=member, active_profile=True)


@app.route("/modal")
def modal():
    return render_template("modal.html")


@app.route("/member/<id>", methods=["POST"])
@admin_login
def modify(id):
    member = Member.objects(pk=id)
    app.logger.debug("Fetched member: %s", member)
    app.logger.debug("Form data: %s", request.form)
    update_name = request.form["name"]
    update_email = request.form["email"]
    update_balance = request.form["balance"]
    update_active = request.form.get("active")

    if update_active:
        update_active = True
    else:
        update_active = False

    if update_email == member[0]["email"]:
        updated_member = Member.objects(id=id).update(
            set__name=update_name,
            set__balance=update_balance,
            set__active=update_active,
        )
        app.logger.debug("Updated member: %s", updated_member)
        flash("Data Updated Successfully", "success")

    else:
        flash("Oops! Unable to Save Data", "Danger")
    app.logger.debug("Form data: %s", request.form)

    url = member[0]["username"]
    return redirect(url)


@app.route("/<name>/remove/<id>", methods=["POST"])
@admin_login
def remove(name, id):
    if name == "members":
        user = Member.objects(id=id)
        if user[0]["admin"]:
            flash("Cannot Remove admin", "danger")
            return {"name": "members", "message": "Cannot Remove admin"}
        else:
            user[0].delete()
            flash("User Deleted SuccessFully", "danger")
            return {"name": "members", "message": "user deleted successfully"}

    elif name == "books":
        Book.objects(id=id).delete()
        flash("Book Deleted SuccessFully", "danger")
        return {"name": "books", "message": "book deleted successfully"}


@app.route("/books/modify/<id>", methods=["POST"])
@admin_login
def modify_book(id):
    data = request.form
    print(data)
    quantity = request.form.get("quantity")
    available = request.form.get("active")
    print("available1=", available)
    if available:
        available = True
    else:
        available = False

    print("available2=", available)

    book = Book.objects(id=id)[0]
    book.update(set__stock=quantity, set__available=available)

    flash("Book Data Modified Sucessfully", "success")
    return redirect(url_for("books"))


@app.route("/book/rent-out/<id>", methods=["POST"])
@admin_login
def rent_book(id):
    data = request.get_data().decode("utf-8")
    data = json.loads(data)

    print(data["user"], id)

    user_email = data["user"]
    member = Member.objects(email=user_email)
    print(member, bool(member))
    if member:
        member = member[0]
        book = Book.objects(id=id)[0]
        stock = book["stock"]
        available = book["available"]
        if stock > 1:
            if member["balance"] > 80 and member["active"]:
                issue_count = book["issue_count"] + 1
                stock = stock - 1

                if stock == 0:
                    available = False
                book.update(
                    set__issue_count=issue_count,
                    set__stock=stock,
                    set__available=available,
                )

                updated_balance = member["balance"] - 50
                updated_total_purchased = member["total_purchased"] + 50
                member.update(
                    add_to_set__current_book=[id],
                    set__balance=updated_balance,
                    set__total_purchased=updated_total_purchased,
                )

                transaction = Transaction(
                    book=book["title"], member=member["name"], borrow=True
                )
                transaction.save()
                flash("Book Issued Successfully", "success")
            else:
                flash("Book not Issued", "danger")
                flash(
                    "Member Account is not Active / Balance is less than minimun required",
                    "danger",
                )
        else:
            flash("Book is not available", "danger")
    else:
        flash("User not found", "danger")

    return {"status": "Success"}


@app.route("/book/return", methods=["POST"])
@admin_login
def book_return():
    data = request.get_data().decode("utf-8")
    data = json.loads(data)

    user = data["user"]
    book_name = data["book"]
    book_id = data["id"]

    # print(book_id, type(book_id))

    book_db = Book.objects(id=book_id).first()
    book_db_id = book_db["id"]

    # print(book_db_id, type(book_db_id))

    member = Member.objects(username=user)[0]

    if member["balance"] > 30 and member["active"]:
        updated_balance = member["balance"] - 30
        updated_total_purchased = member["total_purchased"] + 30

        member.update(
            pull__current_book=book_db_id,
            add_to_set__issued_books=[book_db_id],
            set__balance=updated_balance,
            set__total_purchased=updated_total_purchased,
        )

        transaction = Transaction(book=book_name, member=member["name"], borrow=False)
        transaction.save()

        flash("Book Returned Successfully", "success")
    else:
        flash("Book not Returned", "danger")
        flash(
            "Member Account is not Active / Balance is less than minimun required",
            "danger",
        )

    return {"username": user}


@app.route("/transactions")
@admin_login
def transactions():
    transactions = Transaction.objects()
    return render_template(
        "transactions.html", transactions=transactions, active_transactions=True
    )
