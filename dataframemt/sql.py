import sqlalchemy as _sa

def table_sql(table_name, schema_name=None):
    return table_name if schema_name is None else '{}.{}'.format(schema_name, table_name)


# ----- functions dealing with sql queries to overcome OperationalError -----


def run_func(func, *args, nb_trials=3, logger=None, **kwargs):
    '''Attempt to run a function a number of times to overcome OperationalError exceptions.

    :Parameters:
        func : function
            function to be invoked
        args : sequence
            arguments to be passed to the function
        nb_trials: int
            number of query trials
        logger: logging.Logger or None
            logger for debugging
        kwargs : dict
            keyword arguments to be passed to the function
    '''
    for x in range(nb_trials):
        try:
            return func(*args, **kwargs)
        except (_se.DatabaseError, _se.OperationalError, _ps.OperationalError) as e:
            if logger:
                with logger.scoped_warn("Ignored an exception raised by failed attempt {}/{} to execute `{}.{}()`".format(x+1, nb_trials, func.__module__, func.__name__)):
                    logger.warn_last_exception()
    raise RuntimeError("Attempted {} times to execute `{}.{}()` but failed.".format(nb_trials, func.__module__, func.__name__))


def list_schemas(conn, nb_trials=3, logger=None):
    '''Lists all schemas.

    Parameters
    ----------
        conn : sqlalchemy.engine.base.Engine
            an sqlalchemy connection engine created by function `create_engine()`
        nb_trials: int
            number of query trials
        logger: logging.Logger or None
            logger for debugging

    Returns
    -------
        out : list
            list of all schema names
    '''
    return run_func(_sa.inspect, conn, nb_trials=nb_trials, logger=logger).get_schema_names()


def list_tables(schema_name, conn, nb_trials=3, logger=None):
    '''Lists all tables of a given schema.

    Parameters
    ----------
        schema_name : str
            a valid schema name returned from `list_schemas()`
        conn : sqlalchemy.engine.base.Engine
            an sqlalchemy connection engine created by function `create_engine()`
        nb_trials: int
            number of query trials
        logger: logging.Logger or None
            logger for debugging

    Returns
    -------
        out : list
            list of all table names
    '''
    return run_func(conn.table_names, nb_trials=nb_trials, logger=logger, schema=schema_name)


