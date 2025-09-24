from data import ensure_csv
from clerk import clerk_menu
from teacher import teacher_menu
from hod import hod_menu

def main():
    ensure_csv()
    while True:
        print("\nLogin as: 1) Clerk  2) Teacher  3) HOD  4) Exit")
        choice=input("Choice: ")
        if choice=="1": clerk_menu()
        elif choice=="2": teacher_menu()
        elif choice=="3": hod_menu()
        elif choice=="4": break
        else: print("Invalid choice.")

if __name__=="__main__":
    main()
