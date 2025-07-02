import typer
from .app import create_app
from .models import db, User, Journey, Step

app = create_app()

cli = typer.Typer(help="SkillForge CLI: A tool for managing the application's data.")

@cli.command()
def init_db():
    """Initializes the database by creating all tables."""
    with app.app_context():
        db.create_all()
        typer.secho('Database initialized successfully!', fg=typer.colors.GREEN)

@cli.command()
def create_user(
    username: str = typer.Argument(..., help="Username for the new user."),
    password: str = typer.Option(..., prompt=True, hide_input=True, help="Password for the new user.")
):
    """Creates a new user in the database."""
    with app.app_context():
      
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        typer.secho(f'User "{username}" created successfully!', fg=typer.colors.GREEN)




if __name__ == "__main__":
    cli()
