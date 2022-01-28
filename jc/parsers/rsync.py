"""jc - JSON CLI output utility `rsync` command output parser

Supports the `-i` or `--itemize-changes` option with all levels of
verbosity.

Usage (cli):

    $ rsync -i -a source/ dest | jc --rsync

    or

    $ jc rsync -i -a source/ dest

Usage (module):

    import jc
    result = jc.parse('rsync', rsync_command_output)

    or

    import jc.parsers.rsync
    result = jc.parsers.rsync.parse(rsync_command_output)

Schema:

    [
      {
        "filename":                       string,
        "metadata":                       string,
        "update_type":                    string/null,
        "file_type":                      string/null,
        "checksum_or_value_different":    bool/null,
        "size_different":                 bool/null,
        "modification_time_different":    bool/null,
        "permissions_different":          bool/null,
        "owner_different":                bool/null,
        "group_different":                bool/null,
        "future":                         null,
        "acl_different":                  bool/null,
        "extended_attribute_different":   bool/null
      }
    ]

Examples:

    $ rsync | jc --rsync -p
    []

    $ rsync | jc --rsync -p -r
    []
"""
import re
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`rsync` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'freebsd']
    magic_commands = ['rsync -i', 'rsync --itemize-changes']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool
    # conversions and timestamps

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List = []

    update_type = {
        '<': 'file sent',
        '>': 'file received',
        'c': 'local change or creation',
        'h': 'hard link',
        '.': 'not updated',
        '*': 'message',
        '+': None
    }

    file_type = {
        'f': 'file',
        'd': 'directory',
        'L': 'symlink',
        'D': 'device',
        'S': 'special file',
        '+': None
    }

    checksum_or_value_different = {
        'c': True,
        '.': False,
        '+': None
    }

    size_different = {
        's': True,
        '.': False,
        '+': None
    }

    modification_time_different = {
        't': True,
        '.': False,
        '+': None
    }

    permissions_different = {
        'p': True,
        '.': False,
        '+': None
    }

    owner_different = {
        'o': True,
        '.': False,
        '+': None
    }

    group_different = {
        'g': True,
        '.': False,
        '+': None
    }

    future = None

    acl_different = {
        'a': True,
        '.': False,
        '+': None
    }

    extended_attribute_different = {
        'x': True,
        '.': False,
        '+': None
    }

    if jc.utils.has_data(data):

        file_line_re = re.compile(r'(?P<meta>^[<>ch.*][fdlDS][c.+][s.+][t.+][p.+][o.+][g.+][u.+][a.+][x.+]) (?P<name>.+)')

        for line in filter(None, data.splitlines()):

            file_line = file_line_re.match(line)
            if file_line:
                meta = file_line.group('meta')
                filename = file_line.group('name')

                output_line = {
                    'filename': filename,
                    'metadata': meta,
                    'update_type': update_type[meta[0]],
                    'file_type': file_type[meta[1]],
                    'checksum_or_value_different': checksum_or_value_different[meta[2]],
                    'size_different': size_different[meta[3]],
                    'modification_time_different': modification_time_different[meta[4]],
                    'permissions_different': permissions_different[meta[5]],
                    'owner_different': owner_different[meta[6]],
                    'group_different': group_different[meta[7]],
                    'future': future,
                    'acl_different': acl_different[meta[9]],
                    'extended_attribute_different': extended_attribute_different[meta[10]]
                }

                raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
