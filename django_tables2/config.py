# -*- coding: utf-8 -*-

class RequestConfig(object):
    """
    A configurator that uses request data to setup a table.

    :type paginate: ``dict`` or ``bool``
    :param paginate: indicates whether to paginate, and if so, what default
            values to use. If the value evaluates to ``False``, pagination
            will be disabled. A ``dict`` can be used to specify default values
            for the call to :meth:`.tables.Table.paginate` (e.g. to define a default
            ``per_page`` value).

    """
    def __init__(self, request, paginate=True):
        self.request = request
        self.paginate = paginate

    def configure(self, table):
        """
        Configure a table using information from the request.
        """
        GET = self.request.GET  # makes our lines shorter
        table.order_by = GET.getlist(table.prefixed_order_by_field)
        if self.paginate:
            if hasattr(self.paginate, "items"):
                kwargs = dict(self.paginate)
            else:
                kwargs = {}
            # extract some options from the request
            for x in ("page", "per_page"):
                name = getattr(table, u"prefixed_%s_field" % x)
                if name in self.request.GET:
                    try:
                        kwargs[x] = int(self.request.GET[name])
                    except ValueError:
                        pass
            table.paginate(**kwargs)
