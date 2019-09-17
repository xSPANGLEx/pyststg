import click

from lib import audit


@click.command()
@click.argument("repository")
@click.option("--mode",
              default="strict",
              help="Audit mode [strict] or [permissive]")
def main(repository, mode):
    if mode == "strict":
        opt_mode = audit.AuditMode().strict
    elif opt_mode == "permissive":
        mode = audit.AuditMode().permissive
    else:
        raise audit.UnSupportedModeError(f"UnSupported mode [{opt_mode}]")
    at = audit.Audit(repository, mode=opt_mode)
    results = at.execute()
    for result in results:
        for line in result:
            print(line)


if __name__ == "__main__":
    main()
