import sys
import services
import users


def show_usage():
    print("""
Usage:

  python env_controller.py prepare admin
  python env_controller.py prepare users
  python env_controller.py create users
""")


def main():
    if len(sys.argv) < 3:
        show_usage()
        return

    action = sys.argv[1].lower()
    target = sys.argv[2].lower()

    if action == "prepare":
        if target == "admin":
            services.prepare_admin()
        elif target == "users":
            services.prepare_users()
        else:
            show_usage()

    elif action == "create":
        if target == "users":
            users.create_users()
        else:
            show_usage()

    else:
        show_usage()


if __name__ == "__main__":
    main()