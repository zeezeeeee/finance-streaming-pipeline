SELECT
  name,
  date_format(date_parse(ts, '%Y-%m-%d'), '%Y-%m') AS "year-month",
  AVG(((close_stock - open_stock) / open_stock) * 100) AS avg_monthly_pct_change
FROM cis9760_finance_project
GROUP BY
  name,
  date_format(date_parse(ts, '%Y-%m-%d'), '%Y-%m')
ORDER BY
  name,
  "year-month";
