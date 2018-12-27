import asyncio

import pymongo
from tornado import gen


class StocksMarketDataPrice:
    """This class allows to set and get the price of all the stocks from WRDS. \n" \
    "1. SetStocksPriceInDB is used to save the stock price data in the DB. The inputs " \
    "params (ClientDB, data to save in DB). The data to save is a dictionnary containing: " \
    "{'_id','gvkey','date','curr','csho','vol','adj_factor','price_close','price_high','price_low'," \
    "'return','ret_usd','curr_to_usd','consensus','price_target'} \n 2. GetStocksPriceInDB is used to get all the" \
    " price data saved in DB. The inputs params (ClientDB, query, data to display)."""

    def __init__(self, database, date, *data):
        self.database = database['test']['summary']
        self.data = data

    def __str__(self):
        description = "This class allows to set and get the price of all the stocks from WRDS. \n" \
                      "1. SetStocksPriceInDB is used to save the stock price data in the DB. The inputs " \
                      "params (ClientDB, data to save in DB). The data to save is a dictionnary containing: " \
                      "{'_id','gvkey','date','curr','csho','vol','adj_factor','price_close','price_high','price_low'," \
                      "'return','ret_usd','curr_to_usd','consensus','price_target'} \n 2. GetStocksPriceInDB is used " \
                      "to get all the price data saved in DB. The inputs params (ClientDB, query, data to display)."

        return description

    @gen.coroutine
    def SetStocksPriceInDB(self):
        """
            :param: {'_id','gvkey','date','curr','csho','vol','adj_factor','price_close','price_high',
                    "price_low','return','ret_usd','curr_to_usd','consensus','price_target'}

        """

        yield self.database.insert_many(self.data[0])
        count = yield self.database.count_documents({})
        print("Final count: %d" % count)

    @gen.coroutine
    def GetStocksPriceFromDB(self):
        tab = []
        query = self.data[0]
        display = self.data[1]
        cursor = self.database.find(query, display).sort('date', 1)
        while (yield cursor.fetch_next):
            tab.append(cursor.next_object())

        return tab

    async def SetManyStocksPriceInDB(self):

        await asyncio.wait([self.SetStocksPriceInDB(self.database[data[0]], data[1]) for data in self.data[0]])

    def UpdateStocksPriceInDB(self):

        id = self.data[0]
        newvalue = self.data[1]
        self.database.update_one({'_id': id}, {'$set': newvalue})

    @staticmethod
    async def SetStocksPriceInDB(ClientDB, data):

        try:
            await ClientDB.bulk_write(data)
        except pymongo.errors.BulkWriteError as bwe:
            print(bwe.details)
