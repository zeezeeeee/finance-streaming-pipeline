# Finance Streaming Pipeline

A near real-time data pipeline that streams daily stock price data for 66 publicly traded companies and makes it queryable within minutes of collection.

## Problem

I wanted to practice a genuinely streaming (not batch) data pipeline — one where records land and become queryable continuously, rather than in a single daily dump. Stock price data was a natural fit: constantly updating, easy to source, and meaningful enough to build real analysis on top of.

## Architecture

Alpha Vantage API
│
▼
AWS Lambda (DataTransformer)
pulls daily prices for 66 tickers,
streams each record individually
│
▼
Kinesis Data Stream (Datacollector-stream)
│
▼
Kinesis Firehose (DataCollectorFirehose)
│
▼
S3 (partitioned by date/hour)
│
▼
Glue Crawler → Glue Data Catalog
│
▼
Athena
SQL query: avg monthly % change per company
│
▼
Jupyter Notebook (pandas + matplotlib)
two visualizations


**Services used:** AWS Lambda, Kinesis Data Streams, Kinesis Firehose, S3, Glue, Athena, IAM

## What it does

- Lambda pulls the last 100 trading days of daily price data for each of 66 tickers from the Alpha Vantage API
- Each individual record (not the full batch) is streamed to Kinesis — **6,600 records** streamed successfully in a single run
- Firehose buffers and delivers those records into S3, partitioned by date/hour
- A Glue crawler catalogs the S3 data so it's queryable in Athena
- An Athena query computes the average daily percentage change between opening and closing price, aggregated to the monthly level per company — returned **396 rows** (66 companies × ~6 months)
- Results are pulled into a notebook and visualized

## Visualizations

**Chart 1 — Average daily % change by company:** a horizontal bar chart ranking all 66 companies from lowest to highest average performance, with a zero reference line separating net-positive from net-negative performers.

**Chart 2 — Monthly trend, top 10 vs. bottom 5:** originally intended to show all 66 companies on one line chart, but that produced an unreadable tangle of overlapping lines. Narrowed to the best 10 and worst 5 performers instead, which kept the comparison readable without losing the core insight.

## Notes

- The Lambda function pulls its Alpha Vantage API key from an environment variable rather than hardcoding it
- Built as coursework for Baruch College's CIS9760 (Big Data Technologies)
