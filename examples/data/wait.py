from dogsbody import runtime

print('running task')
print('wait until source remove')

runtime.wait_until_source_remove()
print('now reboot?')
