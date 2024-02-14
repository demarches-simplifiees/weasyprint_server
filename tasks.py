from invoke import task


@task
def black(c):
    print("running black...")
    c.run("black --check .")


@task
def pylint(c):
    print("running pylint...")
    c.run("pylint *.py")


@task(pre=[black, pylint])
def lint(_c):
    print("Linting ... done!")


@task
def test(c):
    print("running tests...")
    c.run("python -m unittest discover")
