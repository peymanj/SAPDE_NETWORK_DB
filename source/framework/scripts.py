user_table_create = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='user' AND xtype='U')
    CREATE TABLE [dbo].[user](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [login] [nvarchar](30) NOT NULL,
        [name] [nvarchar](50) NOT NULL,
        [pass] [nvarchar](200) NOT NULL,
        [is_active] [bit] NOT NULL,
        CONSTRAINT [login_unique] UNIQUE NONCLUSTERED ([login] ASC)
        WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, 
            IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, 
            OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        )
        ON [PRIMARY]

    IF NOT EXISTS (SELECT * FROM [user] WHERE name='superuser')
    INSERT INTO [user] (login, name, pass, access_level) VALUES ('superuser', 'Super User', 'bf077a62b2dffd8add96a92aa5c5efe9', 0);
    IF NOT EXISTS (SELECT * FROM [user] WHERE name='admin')
    INSERT INTO [user] (login, name, pass, access_level) VALUES ('admin', 'System Administrator', 'ddf55f1bf1e2edf05232e268211f9bcd', 1);
"""
# SuperPeym@n
#1

order_table_create = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='order' AND xtype='U')
    CREATE TABLE [dbo].[order](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [code] [nvarchar](50) NOT NULL,
        [date] [date] NULL,
        [total_items] [int] NULL,
        CONSTRAINT [IX_order] UNIQUE NONCLUSTERED 
            ([code] ASC)
        WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY])
        ON [PRIMARY]
"""

check_db_sql = """
    SELECT
        (CASE WHEN (DB_ID(?) IS NOT NULL )
        THEN 'True'
        ELSE 'False'
        END) AS db_exists
"""

create_db_sql = """
    CREATE DATABASE [{}] 
    ALTER DATABASE [{}] MODIFY FILE 
    ( NAME = N'{}', SIZE = 512MB, MAXSIZE = UNLIMITED, FILEGROWTH = 1024KB )
    ALTER DATABASE [{}] MODIFY FILE 
    ( NAME = N'{}_log', SIZE = 256MB, MAXSIZE = UNLIMITED, FILEGROWTH = 10% ) 
"""

login_query = """
    DECLARE @username nvarchar(30)
    SET @username = ?
    DECLARE @password nvarchar(100)
    SET @password = ?

    SELECT 
    CASE 
    WHEN(
        EXISTS(
            SELECT id FROM [user] 
            WHERE login=@username AND pass=@password
            ))
    THEN 
        (SELECT CAST(id AS nvarchar(10)) FROM [user] 
        WHERE login=@username AND pass=@password)
    ELSE 'False'
    END
"""
is_user_active_query = """
    SELECT is_active FROM [user] WHERE id=?
"""

change_password = """
    ALTER LOGIN sa WITH PASSWORD = '{}' OLD_PASSWORD = '{}'
"""

backup_database = """
    BACKUP DATABASE ? TO DISK = ?
"""

restore_database = {
    "su": "ALTER DATABASE {} SET SINGLE_USER WITH ROLLBACK IMMEDIATE;",
    "off": "ALTER DATABASE {} SET OFFLINE;",
    "res": "RESTORE DATABASE ? FROM DISK = ? WITH REPLACE;",
    "on": "ALTER DATABASE {} SET ONLINE;",
    "mu": "ALTER DATABASE {} SET MULTI_USER;",
}

get_constraints = """
    SELECT constraint_name
    FROM (
        SELECT
            t.[name] as [table],         
            c.[type] as constraint_type, 
            isnull(c.[name], i.[name]) as constraint_name
        FROM sys.objects t
        LEFT OUTER JOIN sys.indexes i
            ON t.object_id = i.object_id
        LEFT OUTER JOIN sys.key_constraints c
            ON i.object_id = c.parent_object_id 
            AND i.index_id = c.unique_index_id
        UNION ALL
            SELECT t.[name],
                'DC',
                con.[name]
            FROM sys.default_constraints con
            LEFT OUTER JOIN sys.objects t
                ON con.parent_object_id = t.object_id
            LEFT OUTER JOIN sys.all_columns col
                ON con.parent_column_id = col.column_id
                AND con.parent_object_id = col.object_id) a
    WHERE [table] like '{}' 
        AND (constraint_type LIKE 'UQ' OR constraint_type LIKE 'DC')
"""