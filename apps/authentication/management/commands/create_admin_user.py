from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = "Creates an admin user with the given username and password"

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True, help="Admin username")
        parser.add_argument("--password", required=True, help="Admin password")
        parser.add_argument("--email", required=True, help="Admin email")
        parser.add_argument("--first-name", help="Admin first name")
        parser.add_argument("--last-name", help="Admin last name")

    def handle(self, *args, **options):
        username = options["username"]
        password = options["password"]
        email = options["email"]
        first_name = options.get("first_name", "")
        last_name = options.get("last_name", "")

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            user.is_staff = True
            user.is_superuser = True
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f'Successfully created admin user "{username}"')
            )
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(f'User with username "{username}" already exists')
            )
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Updated password for existing admin user "{username}"'
                )
            )
        except Exception as e:
            raise CommandError(f"Error creating admin user: {e}")
