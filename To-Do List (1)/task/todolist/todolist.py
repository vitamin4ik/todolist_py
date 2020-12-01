# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

today = datetime.today()


def add_new_task(_session, _tasktoadd, _task_deadline=datetime.today()):
    new_row = Table(task=_tasktoadd, deadline=_task_deadline)
    _session.add(new_row)
    _session.commit()
    print("The task has been added!")


def delete_task(_session):
    print("Choose the number of the task you want to delete:")
    rows = _session.query(Table).order_by(Table.deadline.asc()).all()
    print_result_rows(rows, 6)
    task_to_delete = int(input())
    spec_row = rows[task_to_delete - 1]
    _session.delete(spec_row)
    _session.commit()
    print("The task has been deleted!")


def print_tasks(_session, tasks_range):
    rows = None
    actual_pr_format = 0
    if tasks_range == "Today":
        print("")
        print("Today {}:".format(today.strftime('%-d %b')))
        rows = _session.query(Table).filter(Table.deadline == today.date()).order_by(Table.deadline).all()
        actual_pr_format = 1
    elif tasks_range == "Week":
        end_of_week = today.date() + timedelta(days=6)
        rows = _session.query(Table) \
            .filter(Table.deadline.between(today.date().strftime("%Y-%m-%d"), end_of_week.strftime("%Y-%m-%d"))) \
            .order_by(Table.deadline.asc()).all()
        actual_pr_format = 2
    elif tasks_range == "Missed":
        print("")
        print("Missed tasks:")
        rows = _session.query(Table) \
            .filter(Table.deadline < today.date().strftime("%Y-%m-%d")) \
            .order_by(Table.deadline.asc()).all()
        actual_pr_format = 4
    elif tasks_range == "All":
        print("")
        print("All tasks:")
        actual_pr_format = 3
        rows = _session.query(Table) \
            .filter(Table.deadline >= today.date().strftime("%Y-%m-%d")) \
            .order_by(Table.deadline.asc()).all()
    print_result_rows(rows, actual_pr_format)


def print_result_rows(_rows, print_format):
    if print_format == 1:
        if len(_rows) == 0:
            print("Nothing to do!")
        else:
            j = 1
            for t in _rows:
                first_row = t  # In case rows list is not empty
                print("{0}. {1}".format(j, first_row.task))
                j += 1
    elif print_format == 2:
        if len(_rows) == 0:
            for t in range(0, 7, 1):
                day_to_print = today + timedelta(days=t)
                print("")
                print("{}:".format(day_to_print.strftime("%A %-d %b")))
                print("Nothing to do!")
        else:
            icnt = 0
            k = 0
            for t in _rows:
                first_row = t
                if k > 0:
                    if first_row.deadline - today.date() == timedelta(days=icnt):
                        print("{0}. {1}".format(k, first_row.task))
                        k += 1
                        continue
                    else:
                        k = 0
                        icnt += 1
                for i in range(icnt, 7, 1):
                    rr = today.date() + timedelta(days=i)
                    print("")
                    print("{}:".format(rr.strftime("%A %-d %b")))
                    if rr != first_row.deadline:
                        print("Nothing to do!")
                    else:
                        k += 1
                        print("{0}. {1}".format(k, first_row.task))
                        icnt = i
                        break
            for y in range(icnt + 1, 7, 1):
                day_to_print = today + timedelta(days=y)
                print("")
                print("{}:".format(day_to_print.strftime("%A %-d %b")))
                print("Nothing to do!")
        # iterate rows to print out date and then Nothing to do if tasks=0 for this day or list tasks if they are present
    elif print_format in (3, 4, 6):
        if print_format == 4 and len(_rows) == 0:
            print("Nothing is missed!")
        else:
            j = 1
            for t in _rows:
                first_row = t
                idxval = j if print_format in (3, 4) else first_row.id
                print("{0}. {1}. {2}".format(idxval, first_row.task, first_row.deadline.strftime("%-d %b")))
                j += 1


def print_menu():
    print("")
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    return int(input())


if __name__ == '__main__':
    r = print_menu()
    while r != 0:
        if r == 1:
            print_tasks(session, "Today")
        elif r == 2:
            print_tasks(session, "Week")
        elif r == 3:
            print_tasks(session, "All")
        elif r == 4:
            print_tasks(session, "Missed")
        elif r == 5:
            new_task = input("Enter task")
            new_deadline = input("Enter deadline")
            add_new_task(session, new_task, datetime.strptime(new_deadline, "%Y-%m-%d"))
        elif r == 6:
            delete_task(session)

        r = print_menu()
    print("")
    print("Bye")
    exit()

print("Today:")
print("1) Do yoga")
print("2) Make breakfast")
print("3) Learn basics of SQL")
print("4) Learn what is ORM")
