import click

EXCLUDED_API_VALUES = [
    'owner',
    'picture_url',
    'deployed_at',
    'created_at',
    'updated_at',
    'lifecycle_state',
    'id',
    'state',
    'entrypoints',
    'workflow_state'
]


def update_dic_with_set(set_value, dic):
    (key, value) = set_value.split('=')

    __update_dict(key, value, dic)

    return dic


def __update_dict(key, value, dic):
    keys = key.split('.', 1)
    new_key = keys[0]
    index_list = None

    if new_key.find('[') > 0 and new_key.find(']') > 0:
        index_list = int(new_key[new_key.find('[') + 1: new_key.find(']')])
        new_key = new_key[0:new_key.find('[')]

    if len(keys) == 1:
        if index_list == None:
            dic[new_key] = value
        else:
            dic[new_key][index_list] = value
    else:
        if index_list == None:
            __update_dict(keys[1], value, dic[new_key])
        else:
            __update_dict(keys[1], value, dic[new_key][index_list])


def filter_api_values(api_data):
    for key in EXCLUDED_API_VALUES:
        if key in api_data:
            del api_data[key]


def display_dict_differ(dict_differ):
    for diff_tuple in dict_differ:
        if diff_tuple[0] is 'change':
            # click.echo(click.style('- {}: {}'.format(diff_tuple[1], diff_tuple[2][0]), fg='red') + " " + click.style('+ {}: {}'.format(diff_tuple[1], diff_tuple[2][1]), fg='green'))
            click.echo(click.style('- {}: {}'.format(format_key(diff_tuple[1]), diff_tuple[2][0]), fg='red'))
            click.echo(click.style('+ {}: {}'.format(format_key(diff_tuple[1]), diff_tuple[2][1]), fg='green'))
            click.echo()
        elif diff_tuple[0] is 'add' or diff_tuple[0] is 'remove':
            char_action = '+'
            color_action = 'green'

            if diff_tuple[0] is 'remove':
                char_action = '-'
                color_action = 'red'

            if len(diff_tuple[1]) > 0:
                click.echo(click.style('{} {}:'.format(char_action, format_key(diff_tuple[1])), fg=color_action))

            for add_value in diff_tuple[2]:
                # to_display = { 'message': 'diff_key {}', 'var':{'tuple':diff_tuple}}
                message = ''

                if isinstance(add_value[0], int):
                    message = '  {1} {0} {2}'

                elif isinstance(add_value[0], str) and len(diff_tuple[1]) > 0:
                    if isinstance(add_value[1], dict):
                        message = '  {0} {1}: \n    {2}'
                    else:
                        message = '  {0} {1}: {2}'

                elif isinstance(add_value[0], str):
                    message = '{0} {1}: {2}'

                click.echo(click.style(message.format(char_action, add_value[0], add_value[1]), fg=color_action))

            click.echo()
        else:
            click.echo("diff_key {}".format(diff_tuple))


def format_key(key):
    def map_func(x):
        if isinstance(x, int):
            return '[' + str(x) + ']'
        else:
            return x

    if isinstance(key, list):
        return ".".join(map(map_func, key)).replace('.[', '[')
    else:
        return key
