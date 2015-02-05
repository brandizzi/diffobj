
def diff(old, new):
    operations = []
    old_attrs = [a for a in dir(old) if not a.startswith('_')]
    new_attrs = [a for a in dir(new) if not a.startswith('_')]

    for attr in new_attrs:
        new_value = getattr(new, attr)
        if attr not in old_attrs:
           operations.append( ('create', attr, new_value) )
        else:
            old_value = getattr(old, attr)
            if old_value != new_value:
                operations.append( ('update', attr, old_value, new_value) )
            old_attrs.remove(attr)

    for attr in old_attrs:
       operations.append( ('drop', attr) )

    return operations

def patch(base, diff):
    for operation in diff:
        operator, attr = operation[:2]
        if operator in ('create', 'update'):
            value = operation[2]
            if (operator == 'create') and hasattr(base, attr):
                raise Conflict('Attribute {0} already exists.'.format(attr))
            elif operator == 'update':
                curr_value = getattr(base, attr)
                old_value = operation[2]
                if old_value != curr_value:
                    raise Conflict(
                        'Attribute {0} is {1} - expected {2}.'.format(
                            attr, curr_value, old_value
                        )
                    )
                value = operation[3]
            setattr(base, attr, value)
        elif operator == 'drop':
            delattr(base, attr)

class Conflict(Exception):
    pass
