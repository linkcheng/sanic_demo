#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@contact: zheng.long@shoufuyou.com
@module: sanicdb 
@date: 2018-12-28 
"""
import aiomysql
import pymysql


class SanicDB:
    """A lightweight wrapper around aiomysql.Pool for easy to use
    """
    def __init__(self, host, port, db, user, password,
                 loop=None, sanic=None,
                 minsize=3, maxsize=5,
                 return_dict=True,
                 pool_recycle=7*3600,
                 autocommit=True,
                 charset="utf8", **kwargs):
        """
        kwargs: all parameters that aiomysql.connect() accept.
        """
        self.db_args = {
            'host': host,
            'port': port,
            'db': db,
            'user': user,
            'password': password,
            'minsize': minsize,
            'maxsize': maxsize,
            'charset': charset,
            'loop': loop,
            'autocommit': autocommit,
            'pool_recycle': pool_recycle,
        }
        self.sanic = sanic
        if sanic:
            sanic.db = self
        if return_dict:
            self.db_args['cursorclass'] = aiomysql.cursors.DictCursor
        if kwargs:
            self.db_args.update(kwargs)
        self.pool = None

    async def init_pool(self):
        if self.sanic:
            self.db_args['loop'] = self.sanic.loop
        self.pool = await aiomysql.create_pool(**self.db_args)

    async def query(self, query, *parameters, **kwparameters):
        """Returns a row list for the given query and parameters."""
        if not self.pool:
            await self.init_pool()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query, kwparameters or parameters)
                    ret = await cur.fetchall()
                except pymysql.err.InternalError:
                    await conn.ping()
                    await cur.execute(query, kwparameters or parameters)
                    ret = await cur.fetchall()
                return ret

    async def get(self, query, *parameters, **kwparameters):
        """Returns the (singular) row returned by the given query.
        """
        if not self.pool:
            await self.init_pool()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query, kwparameters or parameters)
                    ret = await cur.fetchone()
                except pymysql.err.InternalError:
                    await conn.ping()
                    await cur.execute(query, kwparameters or parameters)
                    ret = await cur.fetchone()
                return ret

    async def execute(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the lastrowid from the query."""
        if not self.pool:
            await self.init_pool()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query, kwparameters or parameters)
                except Exception:
                    # https://github.com/aio-libs/aiomysql/issues/340
                    await conn.ping()
                    await cur.execute(query, kwparameters or parameters)
                return cur.lastrowid

