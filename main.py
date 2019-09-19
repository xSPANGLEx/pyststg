import click

from lib import audit


@click.command()
@click.argument("repository")
def main(repository):
    at = audit.Audit(repository)
    results = at.execute()
    for result in results:
        print(result)


if __name__ == "__main__":
    main()
