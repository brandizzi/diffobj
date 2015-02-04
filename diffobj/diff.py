
def diff(old, new):
    operations = []
    old_attrs = [a for a in dir(old) if not a.startswith('_')]
    new_attrs = [a for a in dir(new) if not a.startswith('_')]

    for attr in new_attrs:
        new_value = getattr(new, attr)
        if attr not in old_attrs:
           operations.append( ('create', attr, new_value) )
        else:
            old_attrs.remove(attr)

    for attr in old_attrs:
       operations.append( ('drop', attr) )

    return operations

def patch(base, diff):
    for operation in diff:
        operator, attr = operation[:2]
        if operator == 'create':
            value = operation[2]
            setattr(base, attr, value)
        elif operator == 'drop':
            delattr(base, attr)
