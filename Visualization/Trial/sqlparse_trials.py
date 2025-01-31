import sqlparse

from sql_metadata import Parser

sql = 'select * from ' \
      'Table1 ' \
      'JOIN Table2 ON Table1.REPORT_NO = Table2.REPORT_NO '


formatted_sql = sqlparse.format(sql, reindent=True, keyword_case='upper')

parser_result = Parser(formatted_sql)
stmt_tokens = parser_result.tokens

# parsed = sqlparse.parse(sql)

# stmt = parsed[0]


# print(sqlparse.format(sql, reindent=True, keyword_case='upper'))

# sqlparse.sql.Identifier(stmt)
i = 0