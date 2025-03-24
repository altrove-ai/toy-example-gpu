# Altrove AI Project template

This project has been initialized by copying the template repository [ai-project-template](https://github.com/altrove-ai/ai-project-template).

## First steps

### Installing dependencies

This project uses [uv](https://github.com/astral-sh/uv) to manage dependencies and tasks. To install it, run:
```bash
# Linux
curl -LsSf https://astral.sh/uv/install.sh | sudo sh

# MacOS
brew install uv

# Otherwise :
pip install uv
```
### Git submodule

The **scripts** folder is a git submodule, i.e. it is a folder that points to another Altrove git repository. In the same manner that you would run ```git pull``` to get changes on your repository, you will need to run :
```bash
git submodule update --remote --merge
```
to get the latest changes on the submodule.

To be more specific, the submodule points to a **specific commit** of the scripts repository. Running the above command will update the commit ID of the submodule (to the latest commit of the scripts repository). That commit ID change can then be commited and pushed to the remote repository.

If you make changes to the scripts by editing files in the submodule folder, you can commit them and push them to the scripts repository by moving to the submodule folder and handling the changes just like you would for any other git repository.
```bash
echo "New file to introduce change to the scripts submodule" > scripts/new_file.txt
cd scripts
git add new_file.txt
git commit -m "Adding new_file.txt"
git push
```




## Pre-commit hooks

This project uses [pre-commit](https://pre-commit.com/) to run code quality checks before committing. The pre-commit checks are mainly
relying on [Ruff](https://github.com/astral-sh/ruff).

To install pre-commit hooks, run:

To add pre-commit hooks to the repository, run:
```bash
pre-commit install
```
Then, you can run pre-commit hooks on staged files by running:
```bash
git add my_file.py  # Staging file
pre-commit run      # Running pre-commit hooks on staged files
```

You can run the pre-commit hooks on all files as well. 
> **WARNING** : Pre-commit will format all files that it sees having issues, and can potentially change files everywhere in your repository, be ready to handle those changes.
```bash
pre-commit run --all-files
```

### Ruff

[Ruff](https://github.com/astral-sh/ruff) is a Python linter that can be used to enforce code quality checks. It is the tool executing the pre-commit checks. It can be ran on its own with :
```bash
uvx ruff check       # Shows errors
uvx ruff check --fix # Shows errors and fixes them if possible
ruff format          # Format files
```