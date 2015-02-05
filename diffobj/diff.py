
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
        operator = operation[0]

        if operator == 'create':
            _create_attr(base, *operation[1:])
        elif operator == 'update':
            _update_attr(base, *operation[1:])
        elif operator == 'drop':
            _drop_attr(base, *operation[1:])

def _create_attr(obj, attr, new_value):
    if hasattr(obj, attr):
        raise Conflict('Attribute {0} already exists.'.format(attr))

    setattr(obj, attr, new_value)

def _update_attr(obj, attr, old_value, new_value):
    if not hasattr(obj, attr):
        raise Conflict('Attribute {0} does not exist.'.format(attr))

    curr_value = getattr(obj, attr)

    if old_value != curr_value:
        raise Conflict(
            'Attribute {0} is {1} - expected {2}.'.format(
                attr, curr_value, old_value
            )
        )

    setattr(obj, attr, new_value)

def _drop_attr(obj, attr):
    delattr(obj, attr)

class Conflict(Exception):
    pass
