from pkg_resources import working_set
from dogsbody import runtime

packages = {}
for dist in list(working_set):
    packages[dist.project_name] = dist.version

length = max([len(name) for name in packages])

with open(runtime.SOURCE.parent / 'infos.txt', 'w') as target:
    for name, version in packages.items():
        target.write('{1:<{0}s} {2}\n'.format(length, name, version))
