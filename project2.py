from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String,text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Engine=create_engine("sqlite:///fintrack.db")
Base=declarative_base()
Session=sessionmaker(bind=Engine)
session=Session()

class Category(Base):
    __tablename__="categories"
    id=Column(Integer,primary_key=True)
    name=Column(String)
    expenses=relationship("Expense",back_populates="category")

class Expense(Base):
    __tablename__="expenses"
    id=Column(Integer,primary_key=True)
    title=Column(String)
    amount=Column(Integer)
    date=Column(String)

    category_id=Column(Integer,ForeignKey("categories.id"))
    category=relationship("Category",back_populates="expenses")
class Subscription(Base):
    __tablename__="subscriptions"
    id=Column(Integer,primary_key=True)
    name=Column(String)
    amount=Column(Integer)
    next_date=Column(String)

class Budget(Base):
    __tablename__="budgets"
    id=Column(Integer,primary_key=True)
    month=Column(String)
    limit=Column(Integer)

Base.metadata.create_all(Engine)


def add_category():
    name=input("category name:-> ")
    session.add(Category(name=name))
    session.commit()
    print("categories added")

def add_expense():
    title = input("Expense title: ")
    amount = int(input("Amount: "))
    date = input("Date (YYYY-MM-DD): ")
    category_id = int(input("Category ID: "))

    session.add(Expense(title=title, amount=amount, date=date, category_id=category_id))
    session.commit()
    print("expense added")

def update_expense():
    update_input=int(input("expense id: "))
    expense=session.query(Expense).filter(Expense.id==update_input).first()
    if expense:
        expense.title = input("New title: ")
        expense.amount = int(input("New amount: "))
        expense.date = input("New date (YYYY-MM-DD): ")
        session.commit()
        print("Expense updated")
    else:
        print("Expense not found")

def delete_expense():
    delete_input= int(input("Expense ID: "))

    expense = session.query(Expense).filter(Expense.id == delete_input).first()

    if expense:
        session.delete(expense)
        session.commit()
        print("Expense deleted")
    else:
        print("Expense not found")

def search_by_date():
    date = input("Enter date (YYYY-MM-DD): ")

    expenses = session.query(Expense).filter(Expense.date == date).all()

    print("Expenses on", date)
    for e in expenses:
        print(e.title, e.amount, e.date)

def add_subscription():
    name = input("Subscription name: ")
    amount = int(input("Amount: "))
    next_date = input("Next date (YYYY-MM-DD): ")

    session.add(Subscription(name=name, amount=amount, next_date=next_date))
    session.commit()

    print("Subscription added")
def set_budget():
    month = input("Month (YYYY-MM): ")
    limit_amount = int(input("Monthly limit: "))

    session.add(Budget(month=month, limit=limit_amount))
    session.commit()

    print("Budget set")

def budget_alert():
    month = input("Month (YYYY-MM): ")


    total = session.execute(
        text("SELECT SUM(amount) FROM expenses WHERE date LIKE :m"), {"m": f"{month}%"}).scalar()

    if total is None:
        total = 0

    budget = session.query(Budget).filter(Budget.month == month).first()

    if budget and total > budget.limit:
        print("Budget exceeded")
        print("Spent:", total, "| Limit:", budget.limit)
    else:
        print("Within budget")
        if budget:
            print("Spent:", total, "| Limit:", budget.limit)
        else:
            print("No budget set for this month.")
while True:
    print("""

1. Add Category
2. Add Expense
3. Update Expense
4. Delete Expense
5. Search Expense by Date

6. Add Subscription
7. Set Monthly Budget
8. Budget Alert
9. Exit
""")

    choice = input("Choose: ")

    if choice == "1":
        add_category()
    elif choice == "2":
        add_expense()
    elif choice == "3":
        update_expense()
    elif choice == "4":
        delete_expense()
    elif choice == "5":
        search_by_date()
    elif choice == "6":
        add_subscription()
    elif choice == "7":
        set_budget()
    elif choice == "8":
        budget_alert()
    elif choice == "9":
        break
    else:
        print("Invalid choice")