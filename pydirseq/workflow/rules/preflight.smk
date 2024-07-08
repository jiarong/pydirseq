
# Directories
dirs = {
    "logs": os.path.join(config["args"]["output"], "logs"),
    "bench": os.path.join(config["args"]["output"], "bench"),
    "results": os.path.join(config["args"]["output"], "results"),
    "envs": os.path.join(workflow.basedir, "envs"),
    "scripts": os.path.join(workflow.basedir, "scripts")
}

for i in ["logs", "bench", "results"]:
    dir = dirs[i]
    os.makedirs(dir, exist_ok=True)

# Targets
targets = [
    #os.path.join(dirs["results"], "example.done")
    os.path.join(dirs["results"], "done.get_cds_cov")
]


# Misc
target_rules = []


def targetRule(fn):
    """Mark rules as target rules for rule print_targets"""
    assert fn.__name__.startswith("__")
    target_rules.append(fn.__name__[2:])
    return fn


def copy_log_file():
    """Concatenate Snakemake log to output log file"""
    import glob

    files = glob.glob(os.path.join(".snakemake", "log", "*.snakemake.log"))
    if files:
        current_log = max(files, key=os.path.getmtime)
        shell("cat " + current_log + " >> " + config["args"]["log"])


onsuccess:
    copy_log_file()

onerror:
    copy_log_file()
