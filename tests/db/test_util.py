import pytest  # type: ignore

from botus_receptus.db import util


class TestDbUtil(object):
    @pytest.fixture
    def mock_db(self, mocker):
        class MockDb(object):
            fetch = mocker.CoroutineMock()
            fetchrow = mocker.CoroutineMock()
            execute = mocker.CoroutineMock()

        return MockDb()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'args,kwargs,expected_query',
        [
            ([], {'table': 'table', 'columns': ['one']}, 'SELECT one FROM table'),
            (
                [],
                {
                    'table': 'table',
                    'columns': ['one', 'two'],
                    'joins': [
                        ('table_two', 'table_two.other_id = table.id'),
                        ('table_three', 'table_three.other_id = table.id'),
                    ],
                },
                'SELECT one, two FROM table JOIN table_two ON table_two.other_id = '
                'table.id JOIN '
                'table_three ON table_three.other_id = table.id',
            ),
            (
                ['one', 'two'],
                {
                    'table': 'table',
                    'columns': ['one', 'two'],
                    'where': ['col1 = $1', 'col2 = $2'],
                },
                'SELECT one, two FROM table WHERE col1 = $1 AND col2 = $2',
            ),
            (
                [],
                {'table': 'table', 'columns': ['one', 'two'], 'order_by': 'col1'},
                'SELECT one, two FROM table ORDER BY col1 ASC',
            ),
            (
                ['one', 'two'],
                {
                    'table': 'table AS t1',
                    'columns': ['t1.one', 't2.two', 't3.three'],
                    'joins': [
                        ('table_two AS t2', 't2.other_id = t1.id'),
                        ('table_three AS t3', 't3.other_id = t1.id'),
                    ],
                    'where': ['t2.col1 = $1', 't3.col2 = $2'],
                    'group_by': ['t1.group1', 't1.group2'],
                    'order_by': 't1.order',
                },
                'SELECT t1.one, t2.two, t3.three FROM table AS t1 '
                'JOIN table_two AS t2 ON t2.other_id = t1.id '
                'JOIN table_three AS t3 ON t3.other_id = t1.id '
                'WHERE t2.col1 = $1 AND t3.col2 = $2 '
                'GROUP BY t1.group1, t1.group2 '
                'ORDER BY t1.order ASC',
            ),
        ],
    )
    async def test_select_all(self, mock_db, args, kwargs, expected_query):
        await util.select_all(mock_db, *args, **kwargs)

        mock_db.fetch.assert_called_once_with(expected_query, *args, record_class=None)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'args,kwargs,expected_query',
        [
            (
                ['one', 'two'],
                {
                    'table': 'table',
                    'columns': ['col1'],
                    'where': ['col1 = $1', 'col2 = $2'],
                },
                'SELECT col1 FROM table WHERE col1 = $1 AND col2 = $2',
            ),
            (
                ['one', 'two'],
                {
                    'table': 'table',
                    'columns': ['col1', 'col2', 'col3'],
                    'where': ['col1 = $1', 'col2 = $2'],
                },
                'SELECT col1, col2, col3 FROM table WHERE col1 = $1 AND col2 = $2',
            ),
            (
                ['one'],
                {
                    'table': 'table',
                    'columns': ['col1', 'col2', 'col3'],
                    'where': ['table.col1 = $1'],
                    'joins': [
                        ('table_two', 'table_two.other_id = table.id'),
                        ('table_three', 'table_three.other_id = table.id'),
                    ],
                },
                'SELECT col1, col2, col3 FROM table JOIN table_two ON '
                'table_two.other_id = table.id JOIN '
                'table_three ON table_three.other_id = table.id '
                'WHERE table.col1 = $1',
            ),
            (
                ['one', 'two'],
                {
                    'table': 'table AS t1',
                    'columns': ['t1.one', 't2.two', 't3.three'],
                    'joins': [
                        ('table_two AS t2', 't2.other_id = t1.id'),
                        ('table_three AS t3', 't3.other_id = t1.id'),
                    ],
                    'where': ['t2.col1 = $1', 't3.col2 = $2'],
                    'group_by': ['t1.group1', 't1.group2'],
                },
                'SELECT t1.one, t2.two, t3.three FROM table AS t1 '
                'JOIN table_two AS t2 ON t2.other_id = t1.id '
                'JOIN table_three AS t3 ON t3.other_id = t1.id '
                'WHERE t2.col1 = $1 AND t3.col2 = $2 '
                'GROUP BY t1.group1, t1.group2',
            ),
        ],
    )
    async def test_select_one(self, mock_db, args, kwargs, expected_query):
        await util.select_one(mock_db, *args, **kwargs)
        mock_db.fetchrow.assert_called_once_with(
            expected_query, *args, record_class=None
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'args,kwargs,expected_query',
        [
            (
                [],
                {
                    'table': 'table',
                    'columns': ['col1'],
                    'search_columns': ['col3'],
                    'terms': ['term1'],
                },
                'SELECT col1 FROM table WHERE '
                "to_tsvector('english', col3) "
                "@@ to_tsquery('english', 'term1')",
            ),
            (
                [],
                {
                    'table': 'table',
                    'columns': ['col1', 'col2'],
                    'search_columns': ['col3', 'col4', 'col5'],
                    'terms': ['term1', 'term2', 'term3'],
                },
                'SELECT col1, col2 FROM table WHERE '
                "to_tsvector('english', col3 || ' ' || col4 || ' ' || col5) "
                "@@ to_tsquery('english', 'term1 & term2 & term3')",
            ),
            (
                ['one', 'two'],
                {
                    'table': 'table',
                    'columns': ['col1', 'col2'],
                    'where': ['col1 = $1', 'col2 = $2'],
                    'search_columns': ['col3'],
                    'terms': ['term1'],
                },
                'SELECT col1, col2 FROM table WHERE col1 = $1 AND col2 = $2 AND '
                "to_tsvector('english', col3) "
                "@@ to_tsquery('english', 'term1')",
            ),
            (
                [],
                {
                    'table': 'table',
                    'columns': ['col1', 'col2'],
                    'joins': [
                        ('table_two', 'table_two.other_id = table.id'),
                        ('table_three', 'table_three.other_id = table.id'),
                    ],
                    'search_columns': ['table.col3'],
                    'terms': ['term1'],
                },
                'SELECT col1, col2 FROM table JOIN table_two ON '
                'table_two.other_id = table.id JOIN '
                'table_three ON table_three.other_id = table.id '
                "WHERE to_tsvector('english', table.col3) "
                "@@ to_tsquery('english', 'term1')",
            ),
            (
                ['one', 'two'],
                {
                    'table': 'table',
                    'columns': ['col1', 'col2'],
                    'where': ['col1 = $1', 'col2 = $2'],
                    'search_columns': ['col3'],
                    'terms': ['term1'],
                },
                'SELECT col1, col2 FROM table WHERE col1 = $1 AND col2 = $2 '
                "AND to_tsvector('english', col3) "
                "@@ to_tsquery('english', 'term1')",
            ),
            (
                [],
                {
                    'table': 'table',
                    'columns': ['col1', 'col2'],
                    'search_columns': ['col3'],
                    'terms': ['term1'],
                    'order_by': 'col1',
                },
                'SELECT col1, col2 FROM table '
                "WHERE to_tsvector('english', col3) "
                "@@ to_tsquery('english', 'term1') "
                'ORDER BY col1 ASC',
            ),
            (
                ['one', 'two'],
                {
                    'table': 'table AS t1',
                    'columns': ['t1.one', 't2.two', 't3.three'],
                    'joins': [
                        ('table_two AS t2', 't2.other_id = t1.id'),
                        ('table_three AS t3', 't3.other_id = t1.id'),
                    ],
                    'where': ['t2.col1 = $1', 't3.col2 = $2'],
                    'search_columns': ['t2.col3', 't3.col4'],
                    'terms': ['term1', 'term2'],
                    'group_by': ['t1.group1', 't1.group2'],
                    'order_by': 't1.order',
                },
                'SELECT t1.one, t2.two, t3.three FROM table AS t1 '
                'JOIN table_two AS t2 ON t2.other_id = t1.id '
                'JOIN table_three AS t3 ON t3.other_id = t1.id '
                'WHERE t2.col1 = $1 AND t3.col2 = $2 '
                "AND to_tsvector('english', t2.col3 || ' ' || t3.col4) "
                "@@ to_tsquery('english', 'term1 & term2') "
                'GROUP BY t1.group1, t1.group2 '
                'ORDER BY t1.order ASC',
            ),
        ],
    )
    async def test_search(self, mock_db, args, kwargs, expected_query):
        await util.search(mock_db, *args, **kwargs)

        mock_db.fetch.assert_called_once_with(expected_query, *args, record_class=None)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'args,kwargs,expected_query',
        [
            (
                [1, '2', 3],
                {'table': 'table', 'values': {'one': '$1', 'two': '$2', 'three': '$3'}},
                'UPDATE table SET one = $1, two = $2, three = $3',
            ),
            (
                [1, '2', 3],
                {
                    'table': 'table',
                    'values': {
                        'one': '$1',
                        'two': '$2::VARCHAR',
                        'three': 'array_append(three, $3)',
                    },
                    'where': ['one = 5'],
                },
                'UPDATE table SET one = $1, two = $2::VARCHAR, three = '
                'array_append(three, $3) WHERE one = 5',
            ),
        ],
    )
    async def test_update(self, mock_db, args, kwargs, expected_query):
        await util.update(mock_db, *args, **kwargs)

        mock_db.execute.assert_called_once_with(expected_query, *args)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'kwargs,expected_query',
        [
            (
                {'table': 'table', 'values': {'one': 1, 'two': '2', 'three': 3}},
                'INSERT INTO table (one, two, three) VALUES ($1, $2, $3)',
            ),
            (
                {
                    'table': 'table',
                    'values': {'one': 1},
                    'extra': 'ON CONFLICT (one) DO UPDATE SET two = EXCLUDED.one',
                },
                'INSERT INTO table (one) VALUES ($1) '
                'ON CONFLICT (one) DO UPDATE SET two = EXCLUDED.one',
            ),
        ],
    )
    async def test_insert_into(self, mock_db, kwargs, expected_query):
        await util.insert_into(mock_db, **kwargs)

        args = [value for value in kwargs['values'].values()]
        mock_db.execute.assert_called_once_with(expected_query, *args)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'args,kwargs,expected_query',
        [
            (
                ['one', 'two'],
                {'table': 'table', 'where': ['col1 = $1', 'col2 = $2']},
                'DELETE FROM table WHERE col1 = $1 AND col2 = $2',
            )
        ],
    )
    async def test_delete_from(self, mock_db, args, kwargs, expected_query):
        await util.delete_from(mock_db, *args, **kwargs)

        mock_db.execute.assert_called_once_with(expected_query, *args)
