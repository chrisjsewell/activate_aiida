[![Anaconda-Server Badge](https://anaconda.org/cjs14/activate-aiida/badges/version.svg)](https://anaconda.org/cjs14/activate-aiida)

# Setting Up AiiDA Environment

This package is designed to achieve the following

1. Conda Environment
   1. (first time only) create it from environment.yml
   2. activate environment
   3. (optional, first time only) pip install local development packages (`pip install --no-deps -e .`)  # TODO
   4. (optional) set branches of local development packages
2. AiiDA Environment
   1. start SQL
   2. (first time only) create SQL User & Database
   3. `rabbitmq-server -detached` (aiida_core >= v1)
   4. `reentry scan -r aiida`
   5. (first time only) create AiiDA Database
   6. (first time only) setup verdi tab completion
   7. start aiida daemon
   8. (optional) import common nodes (created by `verdi export created`)

## Example

conda_environment.yaml:

```yaml
name: aiida_0_12_2_190305
channels:
    - conda-forge
    - cjs14
    - bioconda
    - defaults
dependencies:
    - aiida-core ==0.12.2
    - chainmap ==1.0.2
    - postgresql >=9.4
    - aiida-crystal17 =0.4
    - aiida-quantumespresso ==2.1.1a2
    - jupyter =1.0
    - activate-aiida
```

aiida_environment.yaml:

```yaml
conda_env: aiida_0_12_2_activate
aiida_version: 0.12
aiida_path: /Users/cjs14/GitHub/aiida-cjs-working/databases/aiida/
db_pgsql:
  path: /Users/cjs14/GitHub/aiida-cjs-working/databases/pgsql/aiida_0_12_2_190305
  user: testuser
  user-password: xxxx  # should handle this more securely
  name: testdb
  port: 5432  
db_aiida:
  path: /Users/cjs14/GitHub/aiida-cjs-working/databases/aiida/aiida_0_12_2_190305
  profile: testprofile
  email: chrisj_sewell@hotmail.com
  first-name: chris
  last-name: sewell
  institution: imperial
import_nodes:
  - common_nodes.zip
git_branches:
  - path: /Users/cjs14/GitHub/aiida-lammps
    branch: master
```

Then run:

```console
>> conda env create --file=conda_environment.yaml
>> conda activate aiida_0_12_2_activate
>> source activate-aiida -c -i aiida_environment.yaml
```

## Development Notes

### Conda environment

    >> conda env create --file=path/to/environment.yml
    >> conda activate env_name

TODO: aiida-core should load its [jupyter extension](https://aiida-core.readthedocs.io/en/stable/installation/installation.html#using-aiida-in-jupyter) on installation?

### Pip install local development packages

You can include pip installs in the conda environment.yml.
However, I couldn't see how you could do this for local paths,
and also there is currently no way to set option flags.

We want to use conda packages to satisfy dependencies, so use `--no-deps` flag:

    >> cd path/to/package
    >> pip install --no-deps -e .

We can set the local branch of the package:

    >> git -C path/to/package checkout branch_name

### Setup SQL

    >> pkill postgres
    >> export PGDATA="path/to/database"
    >> initdb
    >> pg_ctl -o "-F -p 5432" start

To test if user exists (from [here](https://stackoverflow.com/a/8546783/5033292)):

    >> psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='testuser'"
    1

To test if database exists (from [here](https://stackoverflow.com/a/17757560/5033292)):

    >> psql -tAc "SELECT 1 FROM pg_database WHERE datname='testdb'"
    1

Then can use in bash as:

```bash
if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='testdb'" )" = '1' ]
then
    echo "Database already exists"
else
    echo "Database does not exist"
fi
```

to create user & db:

    >> createuser testuser
    >> createdb testdb --owner=testuser
    >> psql --dbname=testdb -c "alter user testuser with encrypted password 'niceday';"
    >> psql --dbname=testdb -c "grant all privileges on database testdb to testuser;"

other commands:

    >> psql -l  # to list all databases
    >> psql --dbname=testdb --command="\du+" # to list database users
    >> psql --dbname=testdb --command="\conninfo" # to get the port
    >> dropdb testdb # to delete database
    >> dropuser testuser # to delete user

#### troubleshooting

If postgres is not stopped correctly you may get this error:

    psql: could not connect to server: No such file or directory

In this case you may have to manually delete the
`path/to/database/postmaster.pid` file (see [here](https://stackoverflow.com/a/13573207/5033292))

If a port has been left open (from [here](https://stackoverflow.com/a/17703016/5033292)):

    >> sudo lsof -i :PORTNUM
    >> sudo kill -9 PID

### verdi quicksetup

    >> export AIIDA_PATH="path/to/aiida_config" # must contain .aiida folder
    >> verdi quicksetup --non-interactive --profile testprofile --set-default --email chrisj_sewell@hotmail.com --first-name chris --last-name sewell --institution imperial --backend django --set-default --db-port 5432 --db-user testuser --db-user-pw niceday --db-name testdb --repo "/Users/cjs14/GitHub/aiida-cjs-working/databases/aiida/aiida_0_12_2_190302"
    >> verdi daemon configureuser
    >> verdi daemon start
