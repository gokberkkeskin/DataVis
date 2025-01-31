-- Sample query to be used in DB Comparison tab
select * from
db1.TBL_REPORT_COUNTS
JOIN db2.TBL_REPORT_COUNTS
ON db1.REPORT_NAME = db2.REPORT_NAME