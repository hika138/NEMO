import sqlite3
import datetime

class DBHandler:
    """
    データベースを操作するためのクラス。
    Attributes:
        db (str): データベースファイルのパス。
    """
    def __init__(self, db: str):
        self._db = db
        self._connection = sqlite3.connect(self._db)
        self._cursor = self._connection.cursor()

    @property
    def db(self) -> str:
        return self._db

    def create_table(self, table_name: str, columns: list[tuple[str, str]]) -> None:
        """
        テーブルを作成するメソッド。
        Args:
            table_name (str): 作成するテーブルの名前。
            columns (list[tuple[str, str]]): カラム名とデータ型のリスト。
        """
        columns_def = ', '.join([f"{name} {dtype}" for name, dtype in columns])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def});"
        self._cursor.execute(query)
        self._connection.commit()
    
    def drop_table(self, table_name: str) -> None:
        """
        テーブルを削除するメソッド。
        Args:
            table_name (str): 削除するテーブルの名前。
        """
        query = f"DROP TABLE IF EXISTS {table_name};"
        self._cursor.execute(query)
        self._connection.commit()    
    
    def insert_data(self, table_name: str, data: dict) -> None:
        """
        データを挿入するメソッド。
        Args:
            table_name (str): データを挿入するテーブルの名前。
            data (dict): 挿入するデータの辞書。
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
        self._cursor.execute(query, values)
        self._connection.commit()
        
    def delete_data(self, table_name: str, conditions: list[str]) -> None:
        """
        データを削除するメソッド。
        Args:
            table_name (str): データを削除するテーブルの名前。
            conditions (list[str]): 削除する条件のリスト。
        """
        where_clause = ' AND '.join(conditions)
        query = f"DELETE FROM {table_name} WHERE {where_clause};"
        self._cursor.execute(query)
        self._connection.commit()
    
    def update_data(self, table_name: str, updates: dict, conditions: list[str]) -> None:
        """
        データを更新するメソッド。
        Args:
            table_name (str): データを更新するテーブルの名前。
            updates (dict): 更新するデータの辞書。
            conditions (list[str]): 更新する条件のリスト。
        """
        set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
        where_clause = ' AND '.join(conditions)
        values = tuple(updates.values())
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause};"
        self._cursor.execute(query, values)
        self._connection.commit()

    def select_all(self, table_name: str, column: str = "*") -> list[tuple]:
        """
        テーブルから全てのデータを取得するメソッド。
        Args:
            table_name (str): データを取得するテーブルの名前。
            column (str, optional): 取得するカラム名。デフォルトは"*"。
        Returns:
            list[tuple]: 取得したデータのリスト。
        """
        query = f"SELECT {column} FROM {table_name};"
        self._cursor.execute(query)
        return self._cursor.fetchall()

    def select_where(self, table_name: str, conditions: list[str], column: str = "*") -> list[tuple]:
        """
        条件に基づいてデータを取得するメソッド。
        Args:
            table_name (str): データを取得するテーブルの名前。
            conditions (list[str]): 条件のリスト。
            column (str, optional): 取得するカラム名。デフォルトは"*"。
        Returns:
            list[tuple]: 取得したデータのリスト。
        """
        where_clause = ' AND '.join(conditions)
        query = f"SELECT {column} FROM {table_name} WHERE {where_clause};"
        self._cursor.execute(query)
        return self._cursor.fetchall()
    
    def execute(self, query: str, params: tuple = ()) -> None:
        """
        任意のSQLクエリを実行するメソッド。
        Args:
            query (str): 実行するSQLクエリ。
            params (tuple, optional): クエリのパラメータ。デフォルトは空のタプル。
        """
        self._cursor.execute(query, params)
        self._connection.commit()

    def commit(self) -> None:
        """
        データベースへの変更を保存するメソッド。
        """
        self._connection.commit()

class UtilsDBHandler(DBHandler):
    """
    NEMO用のユーティリティデータベースハンドラクラス。
    
    Args:
        db (str): データベースファイルのパス。
    """
    def __init__(self, db: str):
        super().__init__(db)
    
    def initialize_db(self) -> None:
        """
        NEMOに使うDBの初期化
        """
        # USERSテーブルの作成
        self.create_table(
            "USERS",
            [
                ("ID", "INTEGER PRIMARY KEY NOT NULL"),
                ("DISCORD_ID", "TEXT NOT NULL"),
                ("JOB_ID", "INTEGER NOT NULL"),
                ("CASH", "INTEGER NOT NULL"),
                ("ENERGY", "INTEGER NOT NULL"),
                ("HOUSE_CHANNEL_ID", "INTEGER"),
                ("TELL_THREAD_ID", "INTEGER"),
                ("ACTED_AT", "TEXT")
            ]
        )
        
        # ITEMSテーブルの作成
        self.create_table(
            "ITEMS",
            [
                ("ID", "INTEGER PRIMARY KEY NOT NULL"),
                ("NAME", "TEXT NOT NULL"),
                ("DESCRIPTION", "TEXT"),
                ("TYPE", "TEXT NOT NULL")
            ]
        )
        
        # ITEM_RECIPESテーブルの作成
        self.create_table(
            "ITEM_RECIPES",
            [
                ("ID", "INTEGER PRIMARY KEY NOT NULL"),
                ("ITEM_ID", "INTEGER NOT NULL"),
                ("RECIPE", "TEXT NOT NULL")
            ]
        )
        
        # ITEM_ENERGYテーブルの作成
        self.create_table(
            "ITEM_ENERGY",
            [
                ("ID", "INTEGER PRIMARY KEY NOT NULL"),
                ("ITEM_ID", "INTEGER NOT NULL"),
                ("ENERGY", "INTEGER NOT NULL")
            ]
        )
        
        # INVENTORYテーブルの作成
        self.create_table(
            "INVENTORY",
            [
                ("ID", "INTEGER PRIMARY KEY NOT NULL"),
                ("USER_ID", "INTEGER NOT NULL"),
                ("ITEM_ID", "INTEGER NOT NULL"),
                ("AMOUNT", "INTEGER NOT NULL")
            ]
        )
        
        # MARKETテーブルの作成
        self.create_table(
            "MARKET",
            [
                ("ID", "INTEGER PRIMARY KEY NOT NULL"),
                ("SELLER_ID", "INTEGER NOT NULL"),
                ("ITEM_ID", "INTEGER NOT NULL"),
                ("AMOUNT", "INTEGER NOT NULL"),
                ("PRICE", "INTEGER NOT NULL"),
                ("LISTED_AT", "TEXT NOT NULL")
            ]
        )
        
        # JOBSテーブルの作成
        self.create_table(
            "JOBS",
            [
                ("ID", "INTEGER PRIMARY KEY NOT NULL"),
                ("NAME", "TEXT NOT NULL"),
                ("TOOL_ID", "INTEGER"),
                ("PRODUCT_ID", "INTEGER NOT NULL")
            ]
        )
        
        # TRADE_LOGSテーブルの作成
        self.create_table(
            "TRADE_LOGS",
            [
                ("ID", "INTEGER PRIMARY KEY NOT NULL"),
                ("PROVIDER_ID", "INTEGER NOT NULL"),
                ("RECIPIENT_ID", "INTEGER NOT NULL"),
                ("ITEM_ID", "INTEGER"),
                ("AMOUNT", "INTEGER"),
                ("CASH_AMOUNT", "INTEGER"),
                ("PLACE", "TEXT NOT NULL"),
                ("TRADED_AT", "TEXT NOT NULL")
            ]
        )

    def check_log(self, provider_id: int = 0, recipient_id: int = 0, place: str = "", conditions: list[str] = []) -> str:
        """
        直近の取引ログを確認するメソッド。
        Args:
            provider_id (int, optional): 提供者のID。デフォルトは0。
            recipient_id (int, optional): 受給者のID。デフォルトは0。
            place (str, optional): 取引場所。デフォルトは空文字列。
            conditions (list, optional): 追加の条件。デフォルトは[]。
        Returns:
            str: 直近の取引日時の文字列。ログが存在しない場合は空文字列を返す。
        """
        conds = conditions.copy()
        if provider_id != 0:
            conds.append(f"PROVIDER_ID = {provider_id}")
        if recipient_id != 0:
            conds.append(f"RECIPIENT_ID = {recipient_id}")
        if place != "":
            conds.append(f"PLACE = '{place}'")
        
        results = self.select_where("TRADE_LOGS", conds, "TRADED_AT")
        if not results:
            return ""
        
        # 直近の取引日時を取得
        latest_log = max(results, key=lambda x: x[0])
        return latest_log[0]
    
    def list_items(self, seller_id:int, item_id:int, amount:int, price:int) -> int:
        """
        マーケットにアイテムを出品するメソッド。
        Args:
            seller_id (int): 出品者のID
            item_id (int): アイテムのID
            amount (int): 出品するアイテムの数量
            price (int): アイテムの価格
        """
        self.insert_data("MARKET", 
            {
                "SELLER_ID": seller_id,
                "ITEM_ID": item_id,
                "AMOUNT": amount,
                "PRICE": price,
                "LISTED_AT": datetime.datetime.now().isoformat()
            }
        )
        self.commit()
        return 0

    def buy_items(self, market_id:int, buyer_id:int) -> int:
        """
        マーケットからアイテムを購入するメソッド。
        Args:
            market_id (int): マーケットのID
            buyer_id (int): 購入者のID
        Returns:
            int: 処理結果コード
                0: 購入成功
               -1: マーケットIDが存在しない
               -2: 購入者IDが存在しない
               -3: 所持金不足
        """
        # マーケットからアイテム情報を取得
        market_data = self.select_where("MARKET", [f"ID = {market_id}"])
        if not market_data:
            return -1  # マーケットIDが存在しない場合
        
        seller_id, item_id, amount, price, _ = market_data[0][1:]
        # 購入者の所持金を更新
        buyer_data = self.select_where("USERS", [f"ID = {buyer_id}"])
        if not buyer_data:
            return -2  # 購入者IDが存在しない場合
        buyer_cash = buyer_data[0][3]
        if buyer_cash < price:
            return -3  # 所持金不足
        new_buyer_cash = buyer_cash - price
        self.update_data("USERS", {"CASH": new_buyer_cash}, [f"ID = {buyer_id}"])
        # 出品者の所持金を更新
        seller_data = self.select_where("USERS", [f"ID = {seller_id}"])
        if seller_data:
            seller_cash = seller_data[0][3]
            new_seller_cash = seller_cash + price
            self.update_data("USERS", {"CASH": new_seller_cash}, [f"ID = {seller_id}"])
        # 購入者のインベントリを更新
        inventory_data = self.select_where("INVENTORY", [f"USER_ID = {buyer_id}", f"ITEM_ID = {item_id}"])
        if inventory_data:
            current_amount = inventory_data[0][3]
            new_amount = current_amount + amount
            self.update_data("INVENTORY", {"AMOUNT": new_amount}, [f"USER_ID = {buyer_id}", f"ITEM_ID = {item_id}"])
        else:
            self.insert_data("INVENTORY", {"USER_ID": buyer_id, "ITEM_ID": item_id, "AMOUNT": amount})
        # マーケットからアイテムを削除
        self.delete_data("MARKET", [f"ID = {market_id}"])
        # 取引ログを記録
        self.insert_data("TRADE_LOGS", {
            "PROVIDER_ID": seller_id,
            "RECIPIENT_ID": buyer_id,
            "ITEM_ID": item_id,
            "AMOUNT": amount,
            "PRICE": price,
            "TRADED_AT": datetime.datetime.now().isoformat()
        })
        self.commit()
        return 0