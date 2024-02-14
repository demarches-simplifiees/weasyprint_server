from invoke import task


@task
def ruff_format(c):
    print("running black...")
    c.run("ruff format --check .")


@task
def ruff_lint(c):
    print("running pylint...")
    c.run("ruff check")


@task(pre=[ruff_format, ruff_lint])
def lint(_c):
    print("Linting ... done!")


@task
def test(c):
    print("running tests...")
    c.run("python -m unittest discover")
