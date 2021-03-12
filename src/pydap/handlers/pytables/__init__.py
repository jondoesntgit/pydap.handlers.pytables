"""Pydoop handler for HDF5 files using h5py."""

import os
import re
import time
from stat import ST_MTIME
from email.utils import formatdate

import tables
from pkg_resources import get_distribution

from pydap.model import *
from pydap.handlers.lib import BaseHandler
from pydap.exceptions import OpenFileError

import re
_col_match_re = re.compile('FIELD_\d+_ATTR_')


class HDF5Handler(BaseHandler):

    """A simple handler for HDF5 files based on PyTables."""

    __version__ = get_distribution("pydap.handlers.pytables").version
    extensions = re.compile(r"^.*\.(h5|hdf5)$", re.IGNORECASE)

    def __init__(self, filepath):
        BaseHandler.__init__(self)

        try:
            self.fp = tables.open_file(filepath, 'r')
        except Exception as exc:
            message = 'Unable to open file %s: %s' % (filepath, exc)
            raise OpenFileError(message)

        self.additional_headers.append(
            ('Last-modified', (
                formatdate(
                    time.mktime(
                        time.localtime(os.stat(filepath)[ST_MTIME]))))))

        # build dataset
        name = os.path.split(filepath)[1]
        node = self.fp.root
        self.dataset = DatasetType(name, attributes={
            "NC_GLOBAL": get_attrs(node),
        })
        build_dataset(self.dataset, self.fp, self.fp.root)
        self.fp.close()

def get_attrs(node):
    attrs = {k: node._v_attrs[k] for k in node._v_attrs._v_attrnames
        if k.upper() != k
    }
    return attrs

def build_dataset(target, fp, node):
    """Recursively build a dataset, mapping groups to structures."""
    for node in fp.list_nodes(node):
        if isinstance(node, tables.Group):
            attrs = {k: node._v_attrs[k] for k in node._v_attrs._v_attrnames}
            target[node._v_name] = StructureType(node._v_name, attributes=get_attrs(node)
                    )
            build_dataset(target[node._v_name], fp, node,)
        elif isinstance(node, tables.Array):
            target[node._v_name] = BaseType(
                node._v_name, node, None, attributes=get_attrs(node))

        elif isinstance(node, tables.Table):
            table = node
            table_attrs = {k: v for k, v in get_attrs(node).items() if not _col_match_re.match(k)}
            sequence = target[node._v_name] = SequenceType(node._v_name, attributes=table_attrs)

            for name in table.colnames:
                col_attrs = dict(getattr(table.cols, name).attrs)
                sequence[name] = BaseType(name, table.coldtypes[name], attributes=col_attrs)
            sequence.data = node.read()


if __name__ == "__main__":
    import sys
    from werkzeug.serving import run_simple

    application = HDF5Handler(sys.argv[1])
    run_simple('localhost', 8001, application, use_reloader=True)
