
def diff(old, new):
    operations = []
    old_attributes = [a for a in dir(old) if not a.startswith('_')]
    new_attributes = [a for a in dir(new) if not a.startswith('_')]

    for attr in new_attributes:
        new_value = getattr(new, attr)
        if attr not in old_attributes:
           operations.append( ('create', attr, new_value) )

    return operations

def patch(base, diff):
    for operator, attr, value in diff:
        if operator == 'create':
            setattr(base, attr, value)
