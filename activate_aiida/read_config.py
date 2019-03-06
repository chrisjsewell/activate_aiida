import sys
import os


_COLORRED = '\033[0;31m'
_COLORNONE = '\033[0m'

_CONFIG_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
            "conda_env": {
                "type": "string"
            },
        "aiida_version": {
                "type": "string"
                },
        "db_pgsql": {
                "type": "object",
                "properties": {
                    "user-password": {
                        "type": "string"
                    },
                    "path": {
                        "type": "string"
                    },
                    "user": {
                        "type": "string"
                    },
                    "port": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    }
                },
                "required": [
                    "user-password",
                    "path",
                    "user",
                    "port",
                    "name"
                ]
                },
        "aiida_path": {
                "type": "string"
                },
        "db_aiida": {
                "type": "object",
                "properties": {
                    "profile": {
                        "type": "string"
                    },
                    "last-name": {
                        "type": "string"
                    },
                    "path": {
                        "type": "string"
                    },
                    "first-name": {
                        "type": "string"
                    },
                    "institution": {
                        "type": "string"
                    },
                    "email": {
                        "type": "string"
                    }
                },
                "required": [
                    "profile",
                    "last-name",
                    "path",
                    "first-name",
                    "institution",
                    "email"
                ]
                },
        "import_nodes": {
                "type": "array",
                "items": {
                    "type": "string"
                }
                },
        "git_branches": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "path",
                        "branch"
                    ],
                    "properties": {
                        "path": {"type": "string"},
                        "branch": {"type": "string"},
                    }
                }
                }
    },
    "required": [
        "conda_env",
        "aiida_version",
        "db_pgsql",
        "aiida_path",
        "db_aiida"
    ]
}


def run(sys_args=None):
    try:
        from ruamel.yaml import YAML
    except ImportError:
        sys.stderr.write(
            "{COLORRED}ERROR: ruamel.yaml not installed "
            "(pip install ruamel.yaml){COLORNONE}\n".format(
                COLORRED=_COLORRED, COLORNONE=_COLORNONE))
        sys.exit(1)
    try:
        import jsonschema
    except ImportError:
        sys.stderr.write(
            "{COLORRED}ERROR: jsonschema not installed "
            "(pip install jsonschema){COLORNONE}\n".format(
                COLORRED=_COLORRED, COLORNONE=_COLORNONE))
        sys.exit(1)

    if sys_args is None:
        sys_args = sys.argv[1:]

    fpath = sys_args[0]

    if fpath == "--test":
        return

    if not os.path.exists(fpath):
        sys.stderr.write(
            "{COLORRED}ERROR: could not find path {fpath}{COLORNONE}\n"
            "".format(COLORRED=_COLORRED, COLORNONE=_COLORNONE, fpath=fpath))
        sys.exit(1)
    with open(fpath) as f:
        yaml = YAML(typ='safe')
        config = yaml.load(f)

    try:
        jsonschema.validate(
            config,
            _CONFIG_SCHEMA
        )
    except jsonschema.ValidationError as error:
        sys.stderr.write("{COLORRED}{error}{COLORNONE}\n".format(
            COLORRED=_COLORRED, COLORNONE=_COLORNONE, error=error))
        sys.exit(1)

    outstring = []

    outstring.append(config["conda_env"])
    outstring.append(config["aiida_path"])

    outstring.append(config["db_pgsql"]["path"])
    outstring.append(config["db_pgsql"]["user"])
    outstring.append(config["db_pgsql"]["user-password"])
    outstring.append(config["db_pgsql"]["name"])
    outstring.append(config["db_pgsql"]["port"])

    outstring.append(config["db_aiida"]["path"])
    outstring.append(config["db_aiida"]["profile"])
    outstring.append(config["db_aiida"]["email"])
    outstring.append(config["db_aiida"]["first-name"])
    outstring.append(config["db_aiida"]["last-name"])
    outstring.append(config["db_aiida"]["institution"])

    outstring.append("::".join(config.get("import_nodes", [])))

    gitcommands = []
    for repo in config.get("git_branches", []):
        gitcommands.append(
            "git -C {0} checkout {1}".format(repo["path"], repo["branch"]))
    outstring.append("::".join(gitcommands))

    sys.stdout.write(",".join([str(o) for o in outstring]))
